import argparse
import os
import pathlib
import subprocess
import shutil
import glob
import time
from datetime import datetime
from pathlib import Path

NETARCHS = ["t58-128x10"]

SOUR = "M:\\lczero\\chunks\\"
DATA = "F:\\lczero\\data"
gamefile = str(Path.home()) + '\\.lc0.dat'
lockfile = str(Path.home()) + '\\.lc0.lck'

def get_chunks(data_prefix):
    return glob.glob(data_prefix + "training.*.gz")

def get_oldest_chunks(path, num_chunks):
    chunks = []
    for d in glob.glob(path):
        chunks += get_chunks(d)

    print("sorting {} chunks...".format(len(chunks)), end="")
    chunks.sort(key=os.path.getmtime)
    print("[done]")
    chunks = chunks[:num_chunks]
    print("Moving {} - {}".format(os.path.basename(chunks[0]), os.path.basename(chunks[-1])))
    return chunks

def train(config_file):
    subprocess.run(["python", "train.py", "--cfg", config_file], check=True)

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

def main(cmd):

    if Path(gamefile).exists():
        fg = open(gamefile, "r")
        game_num = int(fg.read())
        fg.close
        file = "training." + str(game_num) + ".gz"
        print("Starting with " + file + " as last game in window")
    else:
        print("File " + gamefile + " must contain a single number ... exiting")
        return

    stopfile = pathlib.Path("stopfile.txt")
    while (True):

        if Path(stopfile).exists():
            print("stopfile exists ... stopping")
            break
            
        if Path(DATA + "\\" + file).exists():
            # update game file so that get_chunks.py can extract next batch
            game_num += cmd.games
            fg = open(gamefile, "w")
            fg.write(str(game_num))
            fg.close()

            # train all networks
            for arch in NETARCHS:
                print("Training " + arch)
                train(arch + ".yaml")
            
            # wait for next cycle
            file = "training." + str(game_num) + ".gz"
            print("Waiting for " + file)
        else:
            os.write(1, b'.')
            time.sleep(60)
        
            

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Starts a training pipeline')
    argparser.add_argument('-g', '--games', type=int, required=True, help="The number of games between training cycles")

    main(argparser.parse_args())
