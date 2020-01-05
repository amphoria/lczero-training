import argparse
import requests
import re
import wget
import os

URL = 'http://data.lczero.org/files/training_data/run2/'
DLDIR = 'M:\\lczero\\files'
DATA = 'F:\\lczero\\data'

def main(cmd):

    if cmd.untar == True:
        print("Training data files will be downloaded to " + DLDIR + " and extracted to " + DATA)
    else:    
        print("Training data files will be downloaded to " + DLDIR)

    html=requests.get(URL)
    url_matches=re.findall('>(' + cmd.files + ')', html.text)

    cwd = os.getcwd()
    os.chdir(DLDIR)

    for url_match in url_matches:
        print(url_match)
        wget.download(URL + url_match)
        print("")
        
        if cmd.untar == True:
            tarfile = 'tar -xvf ' + url_match + ' -C ' + DATA + ' --strip-components 1 2>NUL'
            os.system(tarfile)

    os.chdir(cwd)
	

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download training data from http://data.lczero.org/files/training_data/')
    parser.add_argument('-f', '--files', type=str, required=True, help='regular expression string to select files to download')
    parser.add_argument('-u', '--untar', action='store_true', help='untar downloaded files')
	
    main(parser.parse_args())
	