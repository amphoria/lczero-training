# fetch_games.py

Script to fetch games from data.lczero.org. The games are packaged in TAR files, each containing an hour's games for a particular run. The values for URL, DLDIR and STORE have to be set in the python script.

URL is the url of the directory where the files are stored on data.lczero.org.

DLDIR is the drive and folder to download the TAR files before extraction.

STORE is the drive and folder to extract the game files to. This should normally be different from the folder used by the training pipeline, particularly if your are using start.py.

The extraction of the files relies on GNU Tar for Windows being available somewhere in your Windows PATH as the python library version of TAR doesn't have an option to strip the directory names off the game files.  GNU Tar for Windows can be downloaded from http://gnuwin32.sourceforge.net/packages/gtar.htm.

The script has the following required parameter:

--files=<file name using regular expression wildcards>

The following example would download all of the run 2 files for 1st Oct 2019:

python fetch_games.py --files=training-run2-20191001-[0-9]+.tar




 