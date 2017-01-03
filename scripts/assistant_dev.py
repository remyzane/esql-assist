#!/usr/bin/env python3

import os
import sys
import time
import bottle
from argparse import ArgumentParser, HelpFormatter

import utility
import esql


class CustomizeHelpFormatter(HelpFormatter):
    """Customize ArgumentParser's Help info """

    def add_usage(self, usage, actions, groups, prefix=None):
        sys.stdout.write('%s%s%s' % (usage, os.linesep, os.linesep))

    def format_help(self):
        return None


# run simple server
def do_run():
    bottle.run(app=esql.app, host='0.0.0.0', port=8000)


# run as development mode (automatic reload)
def do_code():
    from watchdog.observers import Observer
    from utility_dev import SourceCodeMonitor, ServerStarter

    # file monitor server
    observer = Observer()

    # py yml file monitor
    patterns = ['*.py', '*esql.toml']  # '*' is necessary, and must in the first.
    restart_processor = ServerStarter([
        # {'cmd': 'rm -rf %s/*.log' % os.path.join(utility.workspace, 'log'), 'is_daemon': False},
        {'cmd': '%s/scripts/assistant_dev.py run' % utility.workspace, 'network_port': (8000,)}
    ])
    monitor = SourceCodeMonitor(restart_processor, patterns)
    observer.schedule(monitor, os.path.join(utility.workspace, 'conf'), recursive=True)
    observer.schedule(monitor, os.path.join(utility.workspace, 'esql'), recursive=True)

    # start monitoring
    observer.start()
    try:
        time.sleep(31536000)  # one year
    except KeyboardInterrupt:
        observer.stop()


if __name__ == '__main__':
    usage = [
        ' ------------------------------ help ------------------------------',
        ' -h                    show help message',
        ' run                   run simple server',
        ' code                  run as development mode (automatic reload)',
    ]
    parser = ArgumentParser(usage=os.linesep.join(usage), formatter_class=CustomizeHelpFormatter)
    parser.add_argument('command', type=str)
    parser.add_argument('-p', '--params', default=[])
    args = parser.parse_args()

    if 'do_' + args.command not in dir():
        parser.print_help()
    else:
        locals()['do_' + args.command](*[] if not args.params else [args.params])
