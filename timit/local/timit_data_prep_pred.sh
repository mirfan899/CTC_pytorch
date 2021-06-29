#!/bin/bash

#This file is used to get the audio path files of the training set, validation set and test set, and the transcription text that is the label file for subsequent processing
#The input parameter is the path of the TIMIT database.
#After replacing the data set, because the data directory structure is inconsistent, this script needs to be modified simply.

if [ $# -ne 2 ]; then
   echo "Need directory of TIMIT dataset !"
   exit 1;
fi

conf_dir=`pwd`/conf
prepare_dir=`pwd`/data
map_file=$conf_dir/phones.60-48-39.map
phoneme_map=$2

. path.sh

>$prepare_dir/predict/wav.scp
>$prepare_dir/predict/wrd_text

# create word text file
for f in $1/predict/*.txt; do
  text=$(cat "$f")
  base=$(basename -- "$f")
  filename="${base%.*}"
  dir="$(dirname "${f}")"
  echo "${filename} ${text}" >> $prepare_dir/predict/wrd_text
done

# create wav_sph.scp for decoding
for f in $1/predict/*.wav; do
  base=$(basename -- "$f")
  filename="${base%.*}"
  dir="$(dirname "${f}")"
  echo "${filename} ${dir}/${base}" >> $prepare_dir/predict/wav.scp
done

python local/generate_phoneme.py --src $prepare_dir/predict/wrd_text --tgt $prepare_dir/predict/phn_text
echo "Data preparation succeeded"
