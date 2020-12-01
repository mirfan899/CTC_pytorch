#!/bin/bash

#The script is to make fbank, mfcc and spectrogram from kaldi

feat_type=$1
data_dir=$2
conf_dir=conf
compress=false

if [[ "$feat_type" != "fbank" && "$feat_type" != "mfcc"  && "$feat_type" != "spectrogram" ]]; then
    echo "Feature type $feat_type does not support!"
    exit 1;
else
    echo ============================================================================
    echo "                $feat_type Feature Extraction and CMVN                    "
    echo ============================================================================

    feat_config=$conf_dir/$feat_type.conf
    if [ ! -f $feat_config ]; then
        echo "missing file $feat_config!"
        exit 1;
    fi

    x=predict
    compute-$feat_type-feats --config=$feat_config scp,p:$data_dir/$x/wav.scp ark:- | \
        apply-cmvn --norm-vars=true $data_dir/global_${feat_type}_cmvn.txt ark:- ark:- |\
            copy-feats --compress=$compress ark:- ark,scp:$data_dir/$x/$feat_type.ark,$data_dir/$x/$feat_type.scp
fi

echo "Finished successfully"
exit 0
