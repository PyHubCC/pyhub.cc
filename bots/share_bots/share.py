import argparse as apa
import configparser
import sys
import logging
import requests as req
import re

CONFIG_FILE = 'config.ini'
ENCODE_MAP = [('%', '@'), (' ', '$')]
logger = logging.getLogger("Tech Share")
logger.setLevel(logging.DEBUG)

def get_title(url):
    res = req.get(url)
    title = re.findall(r'<title>(.*?)<\/title>', res.text)
    return title[0]
def load_config(config_file=CONFIG_FILE):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config
def save_config(config, config_file=CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
def parse_cookie(cookie_str):
    for mp in ENCODE_MAP:
        cookie_str = cookie_str.replace(*mp)
    return cookie_str
def decode_cookie(cookie_str):
    for mp in ENCODE_MAP:
        cookie_str = cookie_str.replace(mp[1], mp[0])
    return cookie_str

def main():
    parser = apa.ArgumentParser()
    parser.add_argument("-H", "--host", help="Add/Update login info of host")
    parser.add_argument("-C", "--cookie", help="Cookie string copied from browser")
    parser.add_argument("-U", "--user", help="Account login user name of host")
    parser.add_argument("-P", "--password", help="Account login user password of host")
    parser.add_argument("-A", "--api", help="Host submit API")

    parser.add_argument("-l", "--link", help="Share a link")
    parser.add_argument("-t", "--tags", help="Tags separated with comma")
    parser.add_argument("--title", help="Shared link's title, parse from link if not given")
    args = parser.parse_args()

    local_config = load_config()
    hosts = local_config.sections()

    if args.host is not None:
        # Update config
        if args.host in hosts:
            # Update
            if args.api:
                local_config[args.host]['API'] = args.api
            if args.user:
                local_config[args.host]['User'] = args.user
            if args.password:
                local_config[args.host]['Password'] = args.password
            if args.cookie:
                local_config[args.host]['Cookie'] = parse_cookie(args.cookie)
        elif not args.api:
            logger.error("[-a, --api] is required!")
            sys.exit(-1)
        else:
            # New entry
            local_config[args.host] = {}
            if args.cookie:
                print(args.cookie.split(";"))
                # local_config[args.host]['Cookie'] = """{}""".format(args.cookie)
            else:
                if not (args.user and args.password):
                    logger.error("You should input both -P and -U")
                    sys.exit(-1)
                local_config[args.host]['User'] = args.user
                local_config[args.host]['Password'] = args.password
        save_config(local_config)
    else:
        if not args.link:
            logger.error("[-l, --link] is required!")
            sys.exit(-1)
        # Share a link
        print("\n分享 [{}]({}) 到:".format(get_title(args.link), args.link))
        print("="*30)
        for i, v in enumerate(hosts):
            print("  ({}) {}".format(i+1, v))
        print("="*30)
        line = input("输入要分享的链接,直接回车全部分享:\n")
        print(line.split(","))

if __name__ == '__main__':
    main()