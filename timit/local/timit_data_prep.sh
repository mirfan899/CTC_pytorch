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
sph2pipe=$KALDI_ROOT/tools/sph2pipe_v2.5/sph2pipe
if [ ! -x $sph2pipe ]; then
   echo "Could not find (or execute) the sph2pipe program at $sph2pipe";
   exit 1;
fi

[ -f $conf_dir/test_spk.list ] || error_exit "$PROG: Eval-set speaker list not found.";
[ -f $conf_dir/dev_spk.list ] || error_exit "$PROG: dev-set speaker list not found.";

#根据数据库train，test的名称修改，有时候下载下来train可能是大写或者是其他形式
train_dir=train
test_dir=test

ls -d "$1"/$train_dir/*/* | sed -e "s:^.*/::" > $conf_dir/train_spk.list

tmpdir=`pwd`/tmp
mkdir -p $tmpdir $prepare_dir
for x in train dev test; do
  if [ ! -d $prepare_dir/$x ]; then
      mkdir -p $prepare_dir/$x
  fi

  # Only use si & sx voice.
  find $1/{$train_dir,$test_dir} -not \( -iname 'SA*' \) -iname '*.WAV' \
    | grep -f $conf_dir/${x}_spk.list > $tmpdir/${x}_sph.flist

  # Get the id of each sentence
  sed -e 's:.*/\(.*\)/\(.*\).WAV$:\1_\2:i' $tmpdir/${x}_sph.flist \
    > $tmpdir/${x}_sph.uttids
  
  # Generate wav.scp, which is the audio path of each sentence
  paste -d" " $tmpdir/${x}_sph.uttids $tmpdir/${x}_sph.flist \
    | sort -k1,1 > $prepare_dir/$x/wav.scp
   
  awk '{printf("%s '$sph2pipe' -f wav %s |\n", $1, $2);}' < $prepare_dir/$x/wav.scp > $prepare_dir/$x/wav_sph.scp

  for y in wrd phn; do
    find $1/{$train_dir,$test_dir} -not \( -iname 'SA*' \) -iname '*.'$y'' \
        | grep -f $conf_dir/${x}_spk.list > $tmpdir/${x}_txt.flist
    sed -e 's:.*/\(.*\)/\(.*\).'$y'$:\1_\2:i' $tmpdir/${x}_txt.flist \
        > $tmpdir/${x}_txt.uttids
    # read wrd file and convert them to simple transcripts
    while read line; do
        [ -f $line ] || error_exit "Cannot find transcription file '$line'";
        cut -f3 -d' ' "$line" | tr '\n' ' ' | sed -e 's: *$:\n:'
    done < $tmpdir/${x}_txt.flist > $tmpdir/${x}_txt.trans
  
    #Put the sentence identifier (uttid) and text label on a line and sort by uttid to make it consistent with the audio path
    paste -d" " $tmpdir/${x}_txt.uttids $tmpdir/${x}_txt.trans \
        | sort -k1,1 > $tmpdir/${x}.trans
  
    #Generate text labels
    cat $tmpdir/${x}.trans | sort > $prepare_dir/$x/${y}_text || exit 1;
    if [ $y == phn ]; then 
        cp $prepare_dir/$x/${y}_text $prepare_dir/$x/${y}_text.tmp
        python local/normalize_phone.py --map $map_file --to $phoneme_map --src $prepare_dir/$x/${y}_text.tmp --tgt $prepare_dir/$x/${y}_text
        rm -f $prepare_dir/$x/${y}_text.tmp
    fi
  done
done

rm -rf $tmpdir

echo "Data preparation succeeded"
