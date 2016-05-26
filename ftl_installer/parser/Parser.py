# -*- coding: utf-8 -*-
import argparse
import ftl_installer
import logging

from ftl_installer.config.Config import Config


class Parser(object):
    ''' The parser. '''
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Ansible based installer framework.')

        self.parser.add_argument('-V', '--version', action='version',
                                 version="ftl_installer-{0}".format(ftl_installer.__version__))

        self.parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                                 default=False, help='show verbose output')

        self.parser.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                                 default=False, help='supress output')

        self.parser.add_argument('-c', '--config', action='store_true',
                                 default=False, help='config file')


def main():  # pragma: no cover
    ''' This is the entrypoint for ftl_installer '''
    parser = Parser()
    args = parser.parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    ftl_logger = logging.getLogger('ftl')
    ftl_logger.setLevel(log_level)

    ftl_stream_handler = logging.StreamHandler() if not args.quiet else logging.NullHandler()
    log_string = "%(message)s"
    ftl_stream_formatter = logging.Formatter(log_string)
    ftl_stream_handler.setFormatter(ftl_stream_formatter)
    ftl_stream_handler.setLevel(log_level)

    ftl_logger.addHandler(ftl_stream_handler)
    ftl_logger.debug("initialized ftl-logging at level: {0}".format(log_level))

    if args.config:
        ftl_config = Config(is_config_file=True)
    else:
        ftl_config = Config()
    print(ftl_config)

    # Do stuff.
    # args.cmd(args)


if __name__ == '__main__':  # pragma: no cover
    main()
