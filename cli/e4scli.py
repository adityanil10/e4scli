import sys
import argparse
import getpass
import requests

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

reset = subparser.add_parser('reset')
list = subparser.add_parser('list')
info = subparser.add_parser('info')
get = subparser.add_parser('get')
set = subparser.add_parser('set')
auth = subparser.add_parser('auth')
power = subparser.add_parser('power')
housekeeping = subparser.add_parser('housekeeping')
watchdog = subparser.add_parser('watchdog')
alert = subparser.add_parser('alert')

reset.add_argument('--id', help='ID is Module ID', type=int)
info.add_argument('id', help='ID is Module ID', type=int)
get.add_argument('id', help='ID is Module ID', type=int)
#get.add_argument('settings', help='To display settings', type=str)
set.add_argument('id', help='ID is Module ID', type=int)
#set.add_argument('settings', help='To update settings', type=str)
#set.add_argument('value', help='Value is setting value', type=int)
auth.add_argument('id', help='ID is Module ID', type=int)
power.add_argument('switch', help='Switch to control power supply of E4S platform', type=str)
power.add_argument('id', help='ID is Module ID', type=int)
#housekeeping.add_argument('function', help='Housekeeping function that is to be controlled on E4S platform', type=str)
watchdog.add_argument('id', help='ID is Module ID', type=int)
alert.add_argument('--id', help='ID is Module ID', type=int)

args: argparse.Namespace = parser.parse_args()


if args.command == 'reset':
    if args.id:
        api_url = 'http://127.0.0.1:5000/smi/reset/{}'.format(args.id)
        response = requests.post(api_url)
        data = response.json()
        print(data['message'])
    else:
        response = requests.get('http://127.0.0.1:5000/smi/reset')
        if response.status_code == 200:
            data = response.json()
            print(data['message'])

elif args.command == 'list':
    response = requests.get('http://127.0.0.1:5000/smi/modules')
    if response.status_code == 200:
        data = response.json()
        print(data)

elif args.command == 'info':
    api_url = 'http://127.0.0.1:5000/smi/modules/{}'.format(args.id)
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        print(data['name'])

elif args.command == 'get':
    api_url = 'http://127.0.0.1:5000/smi/modules/{}/settings'.format(args.id)
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        print(data['message'])

elif args.command == 'set':
    api_url = 'http://127.0.0.1:5000/smi/modules/{}/settings'.format(args.id)
    response = requests.put(api_url)
    if response.status_code == 200:
        data = response.json()
        print(data['message'])

elif args.command == 'auth':
    print('Authentication activated for Module ' + str(args.id))
    password = getpass.getpass('Enter password : ')
    api_url = 'http://127.0.0.1:5000/smi/auth/{}/{}'.format(args.id, password)
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        print(data['message'])
    

elif args.command == 'power':
    if args.switch == 'on':
        api_url = 'http://127.0.0.1:5000/smi/housekeeping/power/on/{}'.format(args.id)
        response = requests.post(api_url)
        if response.status_code == 200:
            data = response.json()
            print(data['message'])
    elif args.switch == 'off':
        api_url = 'http://127.0.0.1:5000/smi/housekeeping/power/off/{}'.format(args.id)
        response = requests.post(api_url)
        if response.status_code == 200:
            data = response.json()
            print(data['message'])
    else:
        print('Invalid argument! It should be either (on/off)')

elif args.command == 'housekeeping':
    response = requests.post('http://127.0.0.1:5000/smi/housekeeping/other')
    if response.status_code == 200:
        data = response.json()
        print(data['message'])

elif args.command == 'watchdog':
    api_url = 'http://127.0.0.1:5000/smi/watchdog/{}'.format(args.id)
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        print(data['message'])

elif args.command == 'alert':
    if args.id:
        api_url = 'http://127.0.0.1:5000/smi/alerts/{}'.format(args.id)
        response = requests.post(api_url)
        if response.status_code == 200:
            data = response.json()
            print(data['message'])
    else:
        response = requests.get('http://127.0.0.1:5000/smi/alerts')
        if response.status_code == 200:
            data = response.json()
            print(data['message'])
