import time
import socket
import logging
import subprocess
from watchdog.events import PatternMatchingEventHandler

log = logging.getLogger(__name__)


def wait_network_port_idle(port):
    """Wait network port idle.

    return after 5 minutes or network port idle.
    TCP connect close TIME_WAIT max 2MSL(2minutes)

    :param port: network port
    """
    for i in range(0, 30):  # 5 minutes
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', port))
            sock.close()        # close effect immediately if not data send
            return
        except Exception:       # OSError
            if i == 0:
                time.sleep(1)   # sometime just need short wait
            else:
                log.info('closing port [%d], Please wait a moment.', port)
                time.sleep(10)
    # import gc
    # from werkzeug.serving import BaseWSGIServer
    # for o in gc.get_referrers(BaseWSGIServer):
    #     if o.__class__ is BaseWSGIServer:
    #         o.server_close()


class SourceCodeMonitor(PatternMatchingEventHandler):
    """source file monitor

    :ivar processor: event processor that have process function
    :ivar maximal_frequency: millisecond, To prevent repeat, IDE/Editor save file is delete and add file
    """
    def __init__(self, processor, patterns, ignore_patterns=None, maximal_frequency=50):
        super(SourceCodeMonitor, self).__init__(
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            ignore_directories=True,    # ignored directory change (delete directory will triggering file delete event)
            case_sensitive=True
        )
        self.processor = processor
        self.maximal_frequency = maximal_frequency
        # last triggering time
        self.last_time = 0

    def on_any_event(self, event):
        # check time interval, To prevent repeat process, IDE/Editor save file is delete and add file
        if time.time()*1000 - self.last_time*1000 < self.maximal_frequency:
            return
        self.processor.process(event.src_path, event.dst_path if hasattr(event, 'dst_path') else None)
        self.last_time = time.time()


class ServerStarter(object):
    """
    :ivar start_commands: e.g.[
                {'cmd': 'xxx', 'is_daemon': True/False, delay: xx, network_port: (xxx,)},
                ...
            ]
        cmd:            command
        is_daemon:      True if command is start daemon server else False
        delay:          seconds, delay start
        network_port:   network port that server running
    """

    def __init__(self, start_commands):
        self.start_commands = start_commands
        self.service_list = []              # process list that running services
        self._start_services(is_first=True)
        log.info('coding server started.')
        log.info('-' * 80)

    def process(self, path, path_moved):
        """Restart server process

        Can't take too long time, when run this function Observer is interrupt.

        :param path: file path that before change
        :param path_moved: file path that after move or add
        """
        log.info('-'*80)
        log.info('restart services for code modify: %s %s', path, path_moved or '')
        self._stop_services()
        self._start_services()

    def _start_services(self, is_first=False):
        for start_cmd in self.start_commands:
            time.sleep(start_cmd.get('delay', 0))
            if 'network_port' in start_cmd:
                for port in start_cmd['network_port']:
                    wait_network_port_idle(port)

            service = subprocess.Popen(start_cmd['cmd'], shell=True)
            if start_cmd.get('is_daemon', True):
                self.service_list.append(service)

        if not is_first:
            log.info('-'*80)

    def _stop_services(self):
        while self.service_list:
            service = self.service_list.pop()
            service.terminate()

    def __del__(self):
        self._stop_services()
