#!/bin/bash
cat /dev/null > output/original.txt
cat /dev/null > output/predicted.txt
cat /dev/null > output/words.txt

cd timit && ./run_pred.sh
