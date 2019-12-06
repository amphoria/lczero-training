import argparse
import requests
import re
import wget
import os

URL = 'http://data.lczero.org/files/training_data/test58/'
DLDIR = 'M:/game_files'
STORE = 'F:/lczero/files'

def main(argv):

    print("Training data files with be downloaded to " + DLDIR + " and then extracted to " + STORE)

    html=requests.get(URL)
    url_matches=re.findall('>(' + argv.files + ')', html.text)

    cwd = os.getcwd()
    os.chdir(DLDIR)

    for url_match in url_matches:
        print(url_match)
        wget.download(URL + url_match)
        tarfile = 'tar -xvf ' + url_match + ' -C ' + STORE + ' --strip-components 1'
        os.system(tarfile)

    os.chdir(cwd)
	

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download training data from http://data.lczero.org/files/training_data/')
    parser.add_argument('--files', type=str, required=True, help='regular expression string to select files to download')
	
    main(parser.parse_args())
	