import argparse
from .conf_manager import BSConf
from .scrapper import Scrapper

get_command_name = 'get'
create_conf_command_name = 'create-conf'


def get_arg_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-q', '--quiet', action='store_true', default=False,
                            help='minimum log and information level')

    subparsers = arg_parser.add_subparsers(dest='command', help="script main command")
    subparsers.required = True

    subparser_search = subparsers.add_parser(get_command_name,
                                             help='retrieve books',
                                             description='retrieve books')
    subparser_search.add_argument('keyword', nargs='+', help='search keywords separated by spaces')

    subparsers.add_parser(create_conf_command_name,
                          help='create the default config file and give its location',
                          description='create the default config file and give its location')

    return arg_parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    verbose_mode = not args.quiet

    bs_conf = BSConf()

    if args.command == create_conf_command_name:
        was_created = bs_conf.create_conf_file()
        if was_created and verbose_mode:
            print('configuration file created {}'.format(bs_conf.conf_path))
        elif not was_created:
            print('configuration file already exists : {}'.format(bs_conf.conf_path))
    else:
        is_conf_ok = bs_conf.check_conf()
        if is_conf_ok:
            scrapper = Scrapper(bs_conf.conf)
            scrapper.scrap(args.keyword, verbose_mode)
        else:
            print('problem with configuration - aborted')


if __name__ == '__main__':
    main()
