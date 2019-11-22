#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Multi Host Updater.
Usage:
  catapult <source_path> <data>
  catapult (-h | --help)
Options:
  -h --help            Show this screen.
  --only=NAME          Only run once.
  --version            Show version.
"""

import sys
import os
import time
import ftplib
import logging
import docopt
import yaml
import tqdm
import colorama

def main(args):
    initiate()
    app = App()

    # Read arguments
    path = args['<source_path>']
    data = args['<data>']
    request = args['--only']

    # Check if package exist
    app.label_secondary('Checking upload folder ', '')
    if os.path.isdir(path) is not True:
        app.label_danger()
        sys.exit()
    else:
        app.label_success()

    # Check if yaml readable
    app.label_secondary('Reading YAML data ', '')
    try:
        data = yaml.safe_load( open(data, 'r') )
    except:
        app.label_danger()
        sys.exit()
    app.label_success()

    # process --only options 
    if request is not None:
        app.label_secondary('Finding data key: ', '')

        if request in data:
            requested_data = data[request]
            data.clear()
            data[request] = requested_data
            app.label_success()
        else:
            app.label_danger()
            sys.exit()

    # Loop through data
    for k in tqdm.tqdm( data.keys() ):	
        
        # sleep(0.1)
        logging.info('Processing ' + data[k]['host'])

        # Preparing ftp
        try:
            ftp = ftplib.FTP(data[k]['host'], data[k]['user'], data[k]['pass']) # open connection
            ftp.cwd( data[k]['path'] ) # changing dir
        except ftplib.all_errors as e:
            errorcode_string = str(e).split(None, 1)[0]
            logging.error('FTP error: ' + str(e))
            continue

        #processing
        try:
            ftp_mput(ftp, path)
        except Exception as e:
            logging.error('FTP error: ' + str(e))
            continue

        # Stopping ftp
        ftp.quit()

class App:
    VER = '1.0.0'

    def label_primary(self, text, endl = '\n'):
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + text + colorama.Style.RESET_ALL, end = endl)

    def label_secondary(self, text, endl = '\n'):
        print(colorama.Style.BRIGHT + colorama.Fore.BLACK + text + colorama.Style.RESET_ALL, end = endl)

    def label_success(self, text='Ok', endl = '\n'):
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + text + colorama.Style.RESET_ALL, end = endl)

    def label_danger(self, text='Fail', endl = '\n'):
        print(colorama.Style.BRIGHT + colorama.Fore.RED + text + colorama.Style.RESET_ALL, end = endl)

    def label_warning(self, text='Warning', endl = '\n'):
        print(colorama.Style.BRIGHT + colorama.Fore.YELLOW + text + colorama.Style.RESET_ALL, end = endl)

    def label_info(self, text, endl = '\n'):
        print(colorama.Fore.CYAN + text + colorama.Style.RESET_ALL, end = endl)

    def label_light(self, text, endl = '\n'):
        print(colorama.Back.BLUE + colorama.Style.BRIGHT + colorama.Fore.YELLOW + text + colorama.Style.RESET_ALL, end = endl)

    def label_dark(self, text, endl = '\n'):
        print(colorama.Back.WHITE + colorama.Style.BRIGHT + colorama.Fore.BLACK + text + colorama.Style.RESET_ALL, end = endl)

def initiate():
    dirname = 'logs'

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    # logging init
    fn = time.strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(filename='logs/' + fn + '.log',level=logging.DEBUG)

# put method for multiple file
def ftp_mput(ftp: ftplib.FTP, path):
    for name in os.listdir(path):

        localpath = os.path.join(path, name)

        if os.path.isfile(localpath):
            ftp.storbinary('STOR ' + name, open(localpath,'rb'))
        elif os.path.isdir(localpath):
            try:
                ftp.mkd(name)
            # ignore "directory already exists"
            except ftplib.error_perm as e:
                if not e.args[0].startswith('550'): 
                    raise

            ftp.cwd(name)
            ftp_mput(ftp, localpath)           
            ftp.cwd("..")

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version=App.VER)
    sys.exit( main(arguments) )