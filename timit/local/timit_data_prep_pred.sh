#!/bin/bash

#此文件用来得到训练集，验证集和测试集的音频路径文件和转录文本即标签文件以便后续处理
#输入的参数时TIMIT数据库的路径。
#更换数据集之后，因为数据的目录结构不一致，需要对此脚本进行简单的修改。

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
