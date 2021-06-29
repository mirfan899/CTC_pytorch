#!/usr/bin/env bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  wget wget https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/download/v1.0.1/montreal-forced-aligner_linux.tar.gz
  tar -xf montreal-forced-aligner_*.tar.gz
  mv montreal-forced-aligner/* .
  rm -rf montreal-forced-aligner
elif [[ "$OSTYPE" == "darwin"* ]]; then
  wget https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/download/v1.0.1/montreal-forced-aligner_macosx.zip
  unzip montreal-forced-aligner_macosx.zip
  mv montreal-forced-aligner/* .
  rm -rf montreal-forced-aligner
elif [[ "$OSTYPE" == "win32" ]]; then
  wget https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/download/v1.0.1/montreal-forced-aligner_win64.zip
  unzip montreal-forced-aligner_win64.zip
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  rm -rf ./lib/thirdparty/bin/libopenblas.so.0
fi