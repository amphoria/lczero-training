import argparse
import glob
import os
import time
from pathlib import Path
from datetime import datetime

DLDIR = 'M:\\lczero\\files\\'
DATA = 'F:\\lczero\\data\\'

gamefile = str(Path.home()) + '\\.lc0.dat'
checkfile = str(Path.home()) + '\\.lc0.file'
lockfile = str(Path.home()) + '\\.lc0.lck'

def lock_chunk_updates(lockfile):
    while Path(lockfile).exists():
        print("Lockfile exists ... sleeping for 60 secs")
        time.sleep(60)
    Path(lockfile).touch(exist_ok=True)

def allow_chunk_updates(lockfile):
    if Path(lockfile).exists():
        Path(lockfile).unlink()

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_files(path):
    return glob.glob(path + "*.tar")

def get_files_sorted(path):
    files = []
    for f in glob.glob(path):
        files += get_files(path)
    files.sort(key=os.path.getmtime)
    return files

def main(cmd):
    cwd = os.getcwd()
    
    if not Path(gamefile).exists():
        print("Game num file (" + gamefile + ") doesn't exist ... exiting")
        return

    if Path(checkfile).exists():
        fc = open(checkfile, "r")
        lastfile = fc.read()
        fc.close()
    else:
        lastfile = ""
    
    os.chdir(DLDIR)

    last_game_num = 0
        
    try:
        while (True):
            # get latest game num ... may have been modified by start.py
            fg = open(gamefile, "r")
            game_num = int(fg.read())
            fg.close()
            
            # check if it has changed
            if game_num != last_game_num:
                last_game_num = game_num
                game_num += cmd.games
                file = "training." + str(game_num) + ".gz"
                print("Looking for " + file)
            else:
                game_num += cmd.games
                file = "training." + str(game_num) + ".gz"
 
            if not Path(DATA + file).exists():
                filelist = get_files_sorted(DLDIR)
                try:
                    fileindex = filelist.index(lastfile)
                    lastindex = len(filelist) - 1
                    if fileindex < lastindex:
                        fileindex += 1
                        lastfile = filelist[fileindex]
                    else:
                        print("No more tar files to process ... sleeping for 5 mins")
                        time.sleep(5*60)
                        continue
                except ValueError:
                    if len(filelist) > 0:
                        fileindex = 0
                    else:
                        print("No more tar files to process ... sleeping for 5 mins")
                        time.sleep(5*60)
                        continue

                # extract files from next tar file
                lock_chunk_updates(lockfile)
                print("Extracting " + filelist[fileindex])
                tarfile = 'tar -xvf ' + filelist[fileindex] + ' -C ' + DATA + ' --strip-components 1 2> NUL'
                os.system(tarfile)
                allow_chunk_updates(lockfile)
                fc = open(checkfile, "w")
                fc.write(lastfile)
                fc.close()
            else:
                print("Game file already present ... sleeping for 5 mins")
                time.sleep(5*60)

    except (KeyboardInterrupt, SystemExit):
        allow_chunk_updates(lockfile)
        os.chdir(cwd)
	

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Move game chunks into training pipeline data folder')
    argparser.add_argument('-g', '--games', type=int, required=True, help="The number of games between training cycles")

    main(argparser.parse_args())
