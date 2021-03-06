## Update:
Works well with Pytorch 1.7 and Python 3.6

## Prediction
For prediction of your own audios and transcripts, place them in Timit/predict directory. Then run the
`run_pred.sh` script to get the results.

# CTC-based Automatic Speech Recognition
This is a CTC-based speech recognition system with pytorch.

At present, the system only supports phoneme recognition.  

You can also do it at word-level and may get a high error rate.

Another way is to decode with a lexicon and word-level language model using WFST which is not included in this system.

## Data
English Corpus: Timit
- Training set: 3696 sentences(exclude SA utterance)
- Dev set: 400 sentences
- Test set: 192 sentences

Chinese Corpus: 863 Corpus
- Training set:
  
|  Speaker |          UtterId         |   Utterances  |  
|   :-:    |           :-:            |      :-:      |  
| M50, F50 |   A1-A521, AW1-AW129     | 650 sentences |    
| M54, F54 | B522-B1040,BW130-BW259   | 649 sentences |   
| M60, F60 | C1041-C1560  CW260-CW388 | 649 sentences |   
| M64, F64 |         D1-D625          | 625 sentences |  
|   All    |                          |5146 sentences |   

- Test set:  

|  Speaker |   UtterId   |   Utterances  |  
|   :-:    |     :-:     |      :-:      |
| M51, F51 |   A1-A100   | 100 sentences | 
| M55, F55 |  B522-B521  | 100 sentences | 
| M61, F61 | C1041-C1140 | 100 sentences | 
| M63, F63 |   D1-D100   | 100 sentences | 
|   All    |             | 800 sentences |

## Install
- Install [Pytorch](http://pytorch.org/)
- ~~Install [warp-ctc](https://github.com/SeanNaren/warp-ctc) and bind it to pytorch.~~  
    ~~Notice: If use python2, reinstall the pytorch with source code instead of pip.~~
    Use pytorch1.2 built-in CTC function(nn.CTCLoss) Now.
- Install [Kaldi](https://github.com/kaldi-asr/kaldi). We use kaldi to extract mfcc and fbank.
- Install pytorch [torchaudio](https://github.com/pytorch/audio.git)(This is needed when using waveform as input).
- ~~Install [KenLM](https://github.com/kpu/kenlm). Training n-gram Languange Model if needed~~.
    Use Irstlm in kaldi tools instead.
- Install and start visdom
```
pip3 install visdom
python -m visdom.server
```
- Install other python packages
```
pip install -r requirements.txt
```

## Usage
1. Install all the packages according to the Install part.  
2. Revise the top script run.sh.  
4. Open the config file to revise the super-parameters about everything.  
5. Run the top script with four conditions
```bash
bash run.sh    #data_prepare + AM training + LM training + testing
bash run.sh 1  #AM training + LM training + testing
bash run.sh 2  #LM training + testing
bash run.sh 3  #testing
```
RNN LM training is not implemented yet. They are added to the todo-list.  

## Data Prepare
1. Extract 39dim mfcc and 40dim fbank feature from kaldi. 
2. Use compute-cmvn-stats and apply-cmvn with training data to get the global mean and variance and normalize the feature. 
3. Rewrite Dataset and dataLoader in torch.nn.dataset to prepare data for training. You can find them in the steps/dataloader.py.

## Model
- RNN + DNN + CTC 
    RNN here can be replaced by nn.LSTM and nn.GRU
- CNN + RNN + DNN + CTC  
    CNN is use to reduce the variety of spectrum which can be caused by the speaker and environment difference.
- How to choose  
    Use add_cnn to choose one of two models. If add_cnn is True, then CNN+RNN+DNN+CTC will be chosen.

## Training:
- initial-lr = 0.001
- decay = 0.5
- wight-decay = 0.005   

Adjust the learning rate if the dev loss is around a specific loss for ten times.  
Times of adjusting learning rate is 8 which can be alter in steps/train_ctc.py(line367).  
Optimizer is nn.optimizer.Adam with weight decay 0.005 

## Decoder
### Greedy decoder:
Take the max prob of outputs as the result and get the path.  
Calculate the WER and CER by used the function of the class.
### Beam decoder:
Implemented with python. [Original Code](https://github.com/githubharald/CTCDecoder)  
I fix it to support phoneme for batch decode.    
Beamsearch can improve about 0.2% of phoneme accuracy.  
Phoneme-level language model is inserted to beam search decoder now.  

## ToDo
- Combine with RNN-LM  
- Beam search with RNN-LM  
- The code in 863_corpus is a mess. Need arranged.

## TIMIT preprocessing
Run this command in `TIMIT` directory. You may need to install `rename` package on Ubuntu.
```shell script
find . -depth -exec rename 's/(.*)\/([^\/]*)/$1\/\L$2/' {} \;
```

Change the timit NIST file to Riff wav
```shell script
find . -name '*.wav' -exec /home/irfan/kaldi/tools/sph2pipe_v2.5/sph2pipe -f wav {} {}.wav \;
# now rename back to original file, be careful dont run it multiple times.
find . -name '*.wav.wav' -exec rename -f 's/.wav.wav/.wav/' -- {} +
```

### Results
timit dataset
```shell script
Character error rate on test set: 13.1404
Word error rate on test set: 19.7505
time used for decode 192 sentences: 1.3049 minutes.
```

timit + librispeech dev dataset
```shell script
Character error rate on test set: 11.7585
Word error rate on test set: 17.5329
time used for decode 192 sentences: 1.1056 minutes.
```

timit + librispeech dev and test dataset.
```shell script
# ongoing.
```

Convert mp3 to required format
```shell
ffmpeg -i dog_3_r2.mp3 -acodec pcm_s16le -ac 1 -ar 16000 dog_3_r2.wav
```

```shell
for i in ./*.mp3; do
  filename=$(basename -- "${i}")
  extension="${filename##*.}"
  name="${filename%.*}"
  ffmpeg -i "$i" -acodec pcm_s16le -ac 1 -ar 16000 "${name}.wav"
done
```

Use CMU stress mark for CTC for all the data
and use aligner for get the phonemes accuracy.

```shell
curl -X POST -F paragraph="When did you come back from your summer camp Lingling I came back last Thursday What did you do there I climbed the mountains and I swam in the river I went fishing one day and caught three fish Really I let them go back into the river again Good for you Was the camp very far No It took only two hours by bus  So you had a lot of fun at the camp Yes I did" -F file=@'test.wav' http://127.0.0.1:5000/api/accuracy
curl -X POST -F paragraph="cheerful hardworking outgoing keen who whose favourite place sport advice to others exhilarated excited frightened interesting excited favourite sport Super Samson Simpson dozen a cold runny nose no energy" -F file=@'output.wav' http://127.0.0.1:5000/api/accuracy
curl -X POST -F paragraph="cheerful hardworking outgoing keen who whose favourite place sport advice to others exhilarated excited frightened interesting excited favourite sport Super Samson Simpson dozen a cold runny nose no energy" -F file=@'output.wav' https://focusmore.ngrok.io/api/accuracy
curl -X POST -F paragraph="Every dog is a mammal. All mammals have hair on their bodies. People, horses, and elephants are also mammals. Hair protects a mammals skin. The hair keeps skin from getting scraped. Hair also protects mammals from cold and heat. What else makes an animal a mammal? Here are some examples. Every mammal has a backbone. That bone is also called the spine. Mammals are warm-blooded. That means the temperature in their bodies is warm and usually stays the same. Female mammals make milk in their bodies. They feed the milk to their babies." -F file=@'test/output.wav' https://focusmore.ngrok.io/api/accuracy
curl -X POST -F paragraph="Every dog is a mammal. All mammals have hair on their bodies. People, horses, and elephants are also mammals. Hair protects a mammals skin. The hair keeps skin from getting scraped. Hair also protects mammals from cold and heat. What else makes an animal a mammal? Here are some examples. Every mammal has a backbone. That bone is also called the spine. Mammals are warm-blooded. That means the temperature in their bodies is warm and usually stays the same. Female mammals make milk in their bodies. They feed the milk to their babies." -F file=@'test/output.wav' http://127.0.0.1:5000/api/accuracy
```

## Necessary Packages for Aligner
```shell script
sudo apt-get install libatlas3-base
sudo apt install libopenblas-dev
```

## Remove object file causing issues on Ubuntu 18
```shell script
rm -rf ./lib/thirdparty/bin/libopenblas.so.0
```
## Another issue
go to montreal force aligner directory and do following
cp lib/libpython3.6m.so.1.0 lib/libpython3.6m.so