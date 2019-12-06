import argparse
import os
import pathlib
import subprocess
import shutil
import glob

NETARCHS = ["dm-128x10"]

SOUR = "F:/lczero/files/"
DEST = "F:/lczero/data"

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
    

def main(cmd):

    stopfile = pathlib.Path("stopfile.txt")
    while (not stopfile.exists()):

        if (not cmd.skipfirstmove):
            # move next game files to data dir
            print("Moving " + str(cmd.games) + " games from " + SOUR + " to " + DEST)
            chunks = get_oldest_chunks(SOUR, cmd.games)

            # stop if not enough chunks
            if (len(chunks) < cmd.games):
                print("Not enough chunks...stopping.")
                break;
            
            for chunk in chunks:
                shutil.move(chunk, DEST)
        else:
            cmd.skipfirstmove = False

        # train all networks
        for arch in NETARCHS:
            print("Training " + arch)
            train(arch + ".yaml")
            

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Starts a training pipeline')
    argparser.add_argument('-g', '--games', type=int, required=True, help="The number of games between training cycles")
    argparser.add_argument('-s', '--skipfirstmove', action='store_true', help="Skip the first file move operation")

    main(argparser.parse_args())
