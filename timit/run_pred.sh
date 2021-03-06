#!/bin/bash

#Author: Ruchao Fan
#2017.11.1     Training acoustic model and decode with phoneme-level bigram
#2018.4.30     Replace the h5py with ark and simplify the data_loader.py
#2019.12.20    Update to pytorch1.2 and python3.7
cat /dev/null > ../output/original.txt
cat /dev/null > ../output/predicted.txt
cat /dev/null > ../output/words.txt

. path.sh

stage=0

timit_dir='../TIMIT'
phoneme_map='60-39'
feat_dir='data'                            #dir to save feature
feat_type='fbank'                          #fbank, mfcc, spectrogram
config_file='conf/ctc_config_pred.yaml'

if [ ! -z $1 ]; then
    stage=$1
fi

if [ $stage -le 0 ]; then
    echo "Step 0: Data Preparation ..."
    local/timit_data_prep_pred.sh $timit_dir $phoneme_map || exit 1;
fi

if [ $stage -le 1 ]; then
    echo "Step 1: Feature Extraction..."
    steps/make_feat_pred.sh $feat_type $feat_dir || exit 1;
fi

if [ $stage -le 2 ]; then
    echo "Step 2: Acoustic Model(CTC) Training..."
fi

if [ $stage -le 3 ]; then
    echo "Step 3: LM Model Training..."
fi

if [ $stage -le 4 ]; then
    echo "Step 4: Decoding..."
    CUDA_VISIBLE_DEVICE='0' python3 steps/pred_ctc.py --conf $config_file || exit 1;
fi

