import ctypes
import json
import os
import random
import tkinter
from tkinter import filedialog
from InquirerPy import inquirer
from InquirerPy.separator import Separator
import colorama


import requests

import checker
from codeparts import checkers, fastcheck as fc, systems, validsort
from codeparts.systems import system

check = checkers.checkers()
sys = systems.system()
valid = validsort.validsort()


class program():
    def __init__(self) -> None:
        self.count = 0
        self.checked = 0
        self.version = '3.11'
        self.riotlimitinarow = 0
        path = os.getcwd()
        self.parentpath = os.path.abspath(os.path.join(path, os.pardir))
        try:
            self.lastver = requests.get(
                'https://api.github.com/repos/lil-jaba/valchecker/releases').json()[0]['tag_name']
        except:
            self.lastver = self.version

    def start(self):
        try:
            print('internet check')
            requests.get('https://github.com')
        except requests.exceptions.ConnectionError:
            print('no internet connection')
            os._exit(0)
        os.system('cls')
        codes = vars(colorama.Fore)
        colors = [codes[color] for color in codes if color not in ['BLACK']]
        colored_name = [random.choice(colors) + char for char in f'ValChecker by liljaba1337']
        print(sys.get_spaces_to_center(f'ValChecker by liljaba1337')+(''.join(colored_name))+colorama.Fore.RESET)
        print(sys.center(f'v{self.version}'))
        if self.lastver != self.version:
            print(sys.center(
                f'\nnext version {self.lastver} is available!'))
            if inquirer.confirm(
                message="{}Would you like to download it now?".format(system.get_spaces_to_center('Would you like to download it now? (Y/n)')), default=True,qmark=''
            ).execute():
                os.system(f'{self.parentpath}/updater.bat')
                os._exit(0)
        menu_choices = [
            Separator(),
            'Start Checker',
            'Edit Settings',
            'Sort Valid',
            'Test Proxy',
            'FastCheck',
            'Info/Help',
            Separator(),
            'Exit'
        ]
        print(sys.center('\nhttps://github.com/LIL-JABA/valchecker\n'))
        res = inquirer.select(
            message="Please select an option:",
            choices=menu_choices,
            default=menu_choices[0],
            pointer='>',
            qmark=''
        ).execute()
        if res == menu_choices[1]:
            self.main(fastcheck=False)
        elif res == menu_choices[2]:
            sys.edit_settings()
            pr.start()
        elif res == menu_choices[3]:
            valid.customsort()
            input('done. press ENTER to exit')
        elif res == menu_choices[4]:
            sys.checkproxy()
            pr.start()
        elif res == menu_choices[5]:
            self.main(fastcheck=True)
        elif res == menu_choices[6]:
            os.system('cls')
            print(f'''
    valchecker v{self.version} by liljaba1337

    discord: LIL JABA#1895
    server: https://discord.gg/r3Y5KhM7kP

  [1] - check valid/invalid/ban and save them to valid.txt in output folder
  [2] - i think u understand
  [3] - sorts all accounts from valid.txt which match your requirements to output\\sorted\\custom.txt
  [4] - test your proxies
  [5] - fast checker (checks only valid/invalid)

  [~] - press ENTER to return
            ''')
            input()
            pr.start()
        elif res == menu_choices[8]:
            os._exit(0)

    def get_accounts(self, filename):
        while True:
            try:
                with open(str(filename), 'r', encoding='UTF-8', errors='replace') as file:
                    lines = file.readlines()
                    # ret=list(set(lines))
                    ret = []
                    if len(lines) > 100000:
                        if inquirer.confirm(
                            message=f"You have more than 100k accounts ({len(lines)}). Do you want to skip the sorting part? (it removes doubles and bad logpasses but can be long)",
                            default=True,
                            qmark='!',
                            amark='!'
                        ).execute():
                            self.count = len(lines)
                            return lines

                    for logpass in lines:
                        logpass = logpass.split(' ')[0].replace(
                            '\n', '').replace(' ', '')
                        # remove doubles
                        if logpass not in ret and ':' in logpass:
                            self.count += 1
                            ctypes.windll.kernel32.SetConsoleTitleW(
                                f'ValChecker {self.version} by liljaba1337 | Loading Accounts ({self.count})')
                            ret.append(logpass)
                    return ret
            except FileNotFoundError:
                print(
                    f"can't find the default file ({filename})\nplease select a new one")
                root = tkinter.Tk()
                file = filedialog.askopenfile(parent=root, mode='rb', title='select file with accounts (login:password)',
                                              filetype=(("txt", "*.txt"), ("All files", "*.txt")))
                root.destroy()
                os.system('cls')
                if file == None:
                    print('you chose nothing')
                    input('press ENTER to choose again')
                    continue
                filename = str(file).split("name='")[1].split("'>")[0]
                with open('system\\settings.json', 'r+') as f:
                    data = json.load(f)
                    data['default_file'] = filename
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                continue

    def main(self, fastcheck=False):
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Settings')
        print('loading settings')
        settings = sys.load_settings()

        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Proxies')
        print('loading proxies')
        proxylist = sys.load_proxy()

        fn = settings['default_file']
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Accounts')
        print('loading accounts')
        accounts = self.get_accounts(fn)

        print('loading assets')
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Assets')
        sys.load_assets()

        if not fastcheck:
            print('loading checker')
            ctypes.windll.kernel32.SetConsoleTitleW(
                f'ValChecker {self.version} by liljaba1337 | Loading Checker')
            scheck = checker.simplechecker(settings, proxylist, sys.useragent)
            scheck.main(accounts, self.count)
            return
        if fastcheck:
            print('loading FastCheck')
            ctypes.windll.kernel32.SetConsoleTitleW(
                f'ValChecker {self.version} by liljaba1337 | Loading FastCheck')
            fch = fc.fastcheck(accounts, self.count, settings, proxylist,sys.useragent)
            fch.main()
            return


pr = program()
if __name__ == '__main__':
    print('starting')
    pr.start()
