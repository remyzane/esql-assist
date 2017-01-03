# -*- coding: utf-8 -*-
import os
import sys
import toml
import cson
import pathlib
import logging

from esql.utility import PY3

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
        self.es_version = None
        self.es_version_major = None
        self.get_elastic_info()
        from elasticsearch import Elasticsearch
        self.es = Elasticsearch(self.es_hosts)
        self.set_elastic_info()
        self.set_libs_path()

    def get_elastic_info(self):
        config = self.config['server']
        driver_version = '2.4.0' if config['driver_version'] == 2 else '5.0.1'
        elastic_package = os.path.join(self.workspace, 'libs', 'elasticsearch-py-' + driver_version)
        if not os.path.exists(elastic_package):
            log.error('elastic package [%s] not exists', elastic_package)
        sys.path.insert(0, elastic_package)

        for host in config['hosts']:
            address, port = host.split(':')
            if address == 'localhost':  # sometimes, 127.0.0.1 localhost not in /etc/hosts
                address = '127.0.0.1'
            self.es_hosts.append({'host': address, 'port': int(port)})

    def set_elastic_info(self):
        from elasticsearch import VERSION
        log.info('load python lib [elasticsearch] with version: %s', VERSION)
        driver_version = self.config['server']['driver_version']
        info = self.es.info()
        self.es_version = info['version']['number']
        self.es_version_major = int(self.es_version.split('.')[0])
        if self.es_version_major != driver_version:
            error = 'elasticsearch\'s version is [%s], but configured python diver\'s version is [%d].'
            log.error(error, self.es_version_major, driver_version)
            exit(0)

    def set_libs_path(self):
        libs = pathlib.Path(os.path.join(self.workspace, 'libs'))
        for lib in libs.iterdir():
            if lib.is_dir() and not lib.name.startswith('elasticsearch-py-'):
                sys.path.insert(0, str(lib))


def load_toml(file_path, prefix=os.curdir):
    if prefix:
        file_path = os.path.join(prefix, file_path)
    if not os.path.exists(file_path):
        raise Exception('toml file [%s] not exists.', file_path)
    f = open(file_path, 'r', encoding='utf-8') if PY3 else open(file_path, 'r')
    data = toml.load(f)
    f.close()
    return data


def load_cson(file_path, prefix=os.curdir):
    if prefix:
        file_path = os.path.join(prefix, file_path)
    if not os.path.exists(file_path):
        raise Exception('cson file [%s] not exists.', file_path)
    f = open(file_path, 'r', encoding='utf-8') if PY3 else open(file_path, 'r')
    data = cson.load(f)
    f.close()
    return data

