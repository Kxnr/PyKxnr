from inspect import currentframe
import logging.config
import logging
import socketserver
import pickle
import struct
from pykxnr.colors import ANSI8ColorPalette

'''
Logging facilities for easy debug logs that telegraph their presence through line numbers/filenames.
Not intended for integration into any production system.
'''


class LoggerTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            try:
                pkt_len, *_ = struct.unpack('>L', self.recv_size(4))
                msg = pickle.loads(self.recv_size(pkt_len))
            except ConnectionError:
                self.finish()
                return

            record = logging.makeLogRecord(msg)
            logging.getLogger('receiver').handle(record)

    def recv_size(self, size):
        msg = b''
        while len(msg) < size:
            msg += self.request.recv(size - len(msg))

            if len(msg) == 0:
                raise ConnectionError("Socket Disconnected")


        return msg


def unpack_log(port=55555):
    with socketserver.ThreadingTCPServer(('127.0.0.1', port), LoggerTCPHandler) as server:
        server.serve_forever()


color_palette = ANSI8ColorPalette(default=7, green=22, error=196, warning=20, debug=216, critical=196, info=7)


class ColoredFormatter(logging.Formatter):
    '''
    take color palette in init and always add palette to _color in record
    '''
    def __init__(self, palette=color_palette, *args, **kwargs):
        self.palette = palette
        super().__init__(*args, **kwargs)

    def format(self, record):
        record._color = self.palette
        return super().format(record)


def debug_print(arg):
    '''
    print function that tags the print with the
    line number and file from which it was called
    so that debug prints can be easily removed
    once they are not needed.

    params
    ------
    '''
    frameinfo = currentframe().f_back
    print(frameinfo.filename, ":", frameinfo.f_lineno, ":", arg)


config_dict = {
    "version": 1,
    "root": {
        "level": "DEBUG",
        "handlers": ["sender"]
    },
    "loggers": {
        "receiver": {
            "level": "DEBUG",
            "handlers": ["receiver"],
            "propagate": False
        }
    },
    "handlers": {
        "sender": {
            "class": "logging.handlers.SocketHandler",
            "level": "DEBUG",
            "formatter": "stack_indicator",
            "host": '127.0.0.1',
            "port": 55555
        },
        "receiver": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored_stack_indicator",
            "stream": "ext://sys.stdout"
        }
    },
    "formatters": {
        "stack_indicator": {
            "format": "{asctime} {levelname: ^8} [{module}:{funcName}:{lineno}] {message}",
            "style": "{"
        },
        "colored_stack_indicator": {
            "()": ColoredFormatter,
            "format": "{_color:green}{asctime}{_color:endcolor} {_color:{levelname}}{levelname: ^8}"
                      + "{_color:endcolor} [{module}:{funcName}:{lineno}] {message}",
            "style": "{",
            "validate": False
        }
    }
}
logging.config.dictConfig(config_dict)

if __name__ == '__main__':
    unpack_log()
