# Training on Windows

The training pipeline resides in `tf`. I have documented the changes I made to get the training pipeline to run under Windows. I have also created some python scripts to help with fetching and processing the self-play game files. 

## Installation

The version of tensorflow used in the training pipeline requires python 3.6. On Windows it is easiest to set up the required python 3.6 environment using Miniconda. My thanks go to dkappe for the first part of this procedure which I obtained from https://github.com/dkappe/leela-chess-weights/wiki/Leela-Chess-Zero-supervised-learning---easy-start-for-Windows-users.

Step 0. Clone or download my fork of LeelaChessZero/lczero-training from https://github.com/amphoria/lczero-training.

Step 1. From the lczero-common page on the LeelaChessZero Github download lczero-common-master.zip and unzip the contents of lczero-common-master into libs\lczero-common. This should now contain one folder called proto.

Step 2. Obtain the protobuf compiler (protoc) for Win64 from the protobuf website https://developers.google.com/protocol-buffers/docs/downloads and unzip protoc.exe into lczero-training. Then run the following commands to compile the protbuf files, and finally create an empty file __init__.py in tf\proto.

```
protoc --proto_path=libs/lczero-common --python_out=tf libs/lczero-common/proto/net.proto
protoc --proto_path=libs/lczero-common --python_out=tf libs/lczero-common/proto/net.proto

```

Step 3. Obtain the Miniconda installer for 64-bit Windows from https://docs.conda.io/en/latest/miniconda.html. It is OK to use the Python 3.7 (or later) version as we will be creating a Python 3.6 environment. Install this following the instructions.

Step 4. Open an Anaconda prompt for Miniconda3 from the Windows start menu and create a python 3.6 environment with the following command:
```
conda create --name py36 python=3.6
```

Step 5. Activate the python 3.6 environment and install Tensorflow for GPU with the following Anaconda commands:
```
conda activate py36
conda install tensorflow-gpu=1.12
```
This will install tensorflow 1.12.2, CUDA, cudnn and any required python packages. tensorflow 1.13 is also supposed to work but I have not tried this. At the end install pyyaml with conda install pyyaml as another version is installed by default.

## Data preparation

In order to start a training session you first need to download trainingdata from http://lczero.org/training_data. This data is packed in tar.gz balls each containing 10'000 games or chunks as we call them. Preparing data requires the following steps:

```
tar -xzf games11160000.tar.gz
ls training.* | parallel gzip {}
```

## Training pipeline

Now that the data is in the right format one can configure a training pipeline. This configuration is achieved through a yaml file, see `training/tf/configs/example.yaml`:

```yaml
%YAML 1.2
---
name: 'kb1-64x6'                       # ideally no spaces
gpu: 0                                 # gpu id to process on

dataset: 
  num_chunks: 100000                   # newest nof chunks to parse
  train_ratio: 0.90                    # trainingset ratio
  # For separated test and train data.
  input_train: '/path/to/chunks/*/draw/' # supports glob
  input_test: '/path/to/chunks/*/draw/'  # supports glob
  # For a one-shot run with all data in one directory.
  # input: '/path/to/chunks/*/draw/'

training:
    batch_size: 2048                   # training batch
    total_steps: 140000                # terminate after these steps
    test_steps: 2000                   # eval test set values after this many steps
    # checkpoint_steps: 10000          # optional frequency for checkpointing before finish
    shuffle_size: 524288               # size of the shuffle buffer
    lr_values:                         # list of learning rates
        - 0.02
        - 0.002
        - 0.0005
    lr_boundaries:                     # list of boundaries
        - 100000
        - 130000
    policy_loss_weight: 1.0            # weight of policy loss
    value_loss_weight: 1.0             # weight of value loss
    path: '/path/to/store/networks'    # network storage dir

model:
  filters: 64
  residual_blocks: 6
...
```

The configuration is pretty self explanatory, if you're new to training I suggest looking at the [machine learning glossary](https://developers.google.com/machine-learning/glossary/) by google. Now you can invoke training with the following command:

```bash
./train.py --cfg configs/example.yaml --output /tmp/mymodel.txt
```

This will initialize the pipeline and start training a new neural network. You can view progress by invoking tensorboard:

```bash
tensorboard --logdir leelalogs
```

If you now point your browser at localhost:6006 you'll see the trainingprogress as the trainingsteps pass by. Have fun!

## Restoring models

The training pipeline will automatically restore from a previous model if it exists in your `training:path` as configured by your yaml config. For initializing from a raw `weights.txt` file you can use `training/tf/net_to_model.py`, this will create a checkpoint for you.

## Supervised training

Generating trainingdata from pgn files is currently broken and has low priority, feel free to create a PR.
