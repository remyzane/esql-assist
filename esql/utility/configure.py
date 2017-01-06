# -*- coding: utf-8 -*-
import os
import sys
import toml
import cson
import pathlib
import logging

log = logging.getLogger(__name__)


class Environment(object):

    def __init__(self):
        try:
            import uwsgi        # run by uWSGI can access the "uwsgi" module (built-in by uWSGI's python plugin)
            workspace = uwsgi.opt['workspace']
        except:
            workspace = os.path.realpath(os.path.join(__file__, '..', '..', '..'))

        self.workspace = workspace
        self.config = load_toml('esql.toml', os.path.join(workspace, 'conf'))

        self.es_hosts = []
        self.es_driver_version = None
        self.conf_elastic()

        self.set_libs_path()
        from elasticsearch import Elasticsearch
        self.es = Elasticsearch(self.es_hosts)

        self.es_version = None
        self.es_version_major = None
        self.get_elastic_version()

    def conf_elastic(self):
        self.es_driver_version = self.config['server']['driver_version']
        for host in self.config['server']['hosts']:
            address, port = host.split(':')
            if address == 'localhost':  # sometimes, 127.0.0.1 localhost not in /etc/hosts
                address = '127.0.0.1'
            self.es_hosts.append({'host': address, 'port': int(port)})

    def set_libs_path(self):
        libs = pathlib.Path(os.path.join(self.workspace, 'libs'))
        for lib in libs.iterdir():
            if lib.is_dir():
                if lib.name.startswith('elasticsearch-py-'):
                    if self.es_driver_version != int(lib.name[len('elasticsearch-py-')]):
                        continue
                sys.path.insert(0, str(lib))

    def get_elastic_version(self):
        from elasticsearch import VERSION
        log.info('load python lib [elasticsearch] with version: %s', VERSION)
        info = self.es.info()
        self.es_version = info['version']['number']
        self.es_version_major = int(self.es_version.split('.')[0])
        if self.es_version_major != self.es_driver_version:
            error = 'elasticsearch\'s version is [%s], but configured python diver\'s version is [%d].'
            log.error(error, self.es_version_major, self.es_driver_version)
            exit(0)


def load_toml(file_path, prefix=os.curdir):
    if prefix:
        file_path = os.path.join(prefix, file_path)
    if not os.path.exists(file_path):
        raise Exception('toml file [%s] not exists.', file_path)
    f = open(file_path, 'r', encoding='utf-8')
    data = toml.load(f)
    f.close()
    return data


def load_cson(file_path, prefix=os.curdir):
    if prefix:
        file_path = os.path.join(prefix, file_path)
    if not os.path.exists(file_path):
        raise Exception('cson file [%s] not exists.', file_path)
    f = open(file_path, 'r', encoding='utf-8')
    data = cson.load(f)
    f.close()
    return data
