import argparse
from tg import TelegramInfo

parser = argparse.ArgumentParser(description='Telegram_OSINT')
parser.add_argument('-a', '--action', help='possible arguments: online', required=True)
parser.add_argument('-u', help='username', default=None)
parser.add_argument('-s', help='seconds between check', default=None)


args = parser.parse_args()
seconds = args.u
username = args.s

if args.action == 'online':
    TG = TelegramInfo()
    if seconds:
        TG.check_every_second = seconds
    TG.is_online(username)
