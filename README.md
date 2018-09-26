# LISA: Linguistically-Informed Self-Attention

This is the original implementation of the linguistically-informed self-attention (LISA) model 
described in the following paper:
> Emma Strubell, Patrick Verga, Daniel Andor, David Weiss, and Andrew McCallum. [Linguistically-Informed 
> Self-Attention for Semantic Role Labeling](https://arxiv.org/abs/1804.08199). 
> *Conference on Empirical Methods in Natural Language Processing (EMNLP)*. 
> Brussels, Belgium. October 2018. 

This code is based on a fork of Timothy Dozat's 
[open source graph-based dependency parser](https://github.com/tdozat/Parser-v1), and the code to run ELMo is copied from
 [AI2's TensorFlow implementation](https://github.com/allenai/bilm-tf). Thanks Tim and AI2!

This code is released for exact replication of the paper. 
**You can find a work-in-progress but vastly improved re-implementation of LISA [here](https://github.com/strubell/LISA).**

Requirements:
----
- Python 2.7
- \>= TensorFlow 1.1
- h5py (for ELMo models)

Quick start:
============

Data setup (CoNLL-2005, GloVe):
----
1. Get pre-trained word embeddings (GloVe):
    ```bash
    wget -P data http://nlp.stanford.edu/data/glove.6B.zip
    unzip -j data/glove.6B.zip glove.6B.100d.txt -d data/glove
    ```
2. Get CoNLL-2005 data in the right format using [this repo](https://github.com/strubell/preprocess-conll05). 
Follow the instructions all the way through [preprocessing for evaluation](https://github.com/strubell/preprocess-conll05#pre-processing-for-evaluation-scripts).
3. **Make sure `data_dir` is set correctly, to the root directory of the data, in any config files you wish to use below.**

Download and evaluate a pre-trained model:
----
Pre-trained models are available for download via Google Drive [here](https://drive.google.com/drive/u/1/folders/1E0Jn05VFqZTbbVcDoM5DEIHEFzD91iLs).

To download the model from Google Drive on the command line, you can use the following bash function (from [here](https://gist.github.com/iamtekeste/3cdfd0366ebfd2c0d805)):
```bash
function gdrive_download () {
  CONFIRM=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=$1" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
  wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$CONFIRM&id=$1" -O $2
  rm -rf /tmp/cookies.txt
}
```
The `gdrive_download` function takes two parameters: Google Drive ID and filename. You can find model names and their
corresponding ids in this table:

| Model                | ID                                  |
| -------------------- | ----------------------------------- |
| `sa-conll05`         | `1Qj5idT0A-OQlN24HRoHAt9G2P-CrW9zb` |
| `lisa-conll05`       | `1XW3qWWMONnQt0lPyj0_t5KdcD7hF8k4F` |
| `sa-conll12`         | `1kGAs73-5HtM9UY4IAHYmFXiyYDQomzo5` |
| `lisa-conll12`       | `1V9-lB-TrOxvProqiJ5Tx1cFUdHkTyjbw` |
|                      |                                     |
| `sa-conll05-elmo`    | `1RX-1YlHQPLRiJGzKF_KHjbNiVCyICRWZ` |
| `lisa-conll05-elmo`  | `1J5wrZUQ7UIVpbZjd7RtbO3EcYE5aRBJ7` |
| `sa-conll12-elmo`    | `1HZ_LTKHa-msrBp73KhdIJvx4tw5UMP2W` |
| `lisa-conll12-elmo`  | `1LbToM5Fbk4yvglvse0X6Q5c0NjHV6HY0` |

To download and evaluate e.g. the `lisa-conll05` model using GloVe embeddings:
```bash
mkdir -p models
gdrive_download 1XW3qWWMONnQt0lPyj0_t5KdcD7hF8k4F models/lisa-conll05.tar.gz
tar xzvf models/lisa-conll05.tar.gz -C models
python network.py --load --test --test_eval --load_dir models/lisa-conll05 --config_file models/lisa-conll05/config.cfg 
```

To evaluate it on the Brown test set:
```bash
python network.py --load --test --test_eval --load_dir models/lisa-conll05 --config_file models/lisa-conll05/config.cfg --test_file $CONLL05/test.brown.gz.parse.sdeps.combined.bio --gold_test_props_file $CONLL05/conll2005-test-brown-gold-props.txt --gold_test_parse_file $CONLL05/conll2005-test-brown-gold-parse.txt
```

Evaluating with ELMo embeddings:
----
First, download the [pre-trained ELMo model and options](https://allennlp.org/elmo) into a directory called `elmo_model`:
```bash
wget -P elmo_model https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5
wget -P elmo_model https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_options.json
```
In order for the model to fit in memory you may want to reduce `max_characters_per_token` to 25 in the options file:
```bash
sed 's/"max_characters_per_token": [0-9][0-9]*/"max_characters_per_token": 25/' elmo_model/elmo_2x4096_512_2048cnn_2xhighway_options.json
```

Run the D&M+ELMo parser
----
Code for running the D&M+ELMo parser that we use in our paper can be found in the `elmo-parser-stable` branch of this repo:
```bash
git checkout elmo-parser-stable
```

If you haven't already, [download the pre-trained ELMo model](#evaluating-with-elmo-embeddings).

Pre-trained parser models are available via [Google Drive](https://drive.google.com/drive/u/1/folders/1E0Jn05VFqZTbbVcDoM5DEIHEFzD91iLs). 
Here are the corresponding ids if you wish to [download via command line](#download-and-evaluate-a-pre-trained-model):

| Model             | ID                                  |
| ----------------- | ----------------------------------- |
| `dm-conll05-elmo` | `1uVJna6ddiJCWelU384ssJrnBJGWlPUML` |
| `dm-conll12-elmo` | `1TQJN0DPxgjCq0fHGZ1Z455fn-ORBENQc` |

To download and evaluate e.g. the `dm-conll05-elmo` parser, you can do the following:
```bash
git checkout elmo-parser-stable
mkdir -p models
gdrive_download 1uVJna6ddiJCWelU384ssJrnBJGWlPUML models/dm-conll05-elmo.tar.gz
tar xzvf models/dm-conll05-elmo.tar.gz -C models
python network.py --load --test --test_eval --load_dir models/dm-conll05-elmo --config_file models/dm-conll05-elmo/config.cfg 
```

Evaluate LISA using the D&M parse
----

Once you've [run the D&M+ELMo parser](#run-the-dmelmo-parser), you may want to provide that parse to LISA.
You can do this by: (1) creating a new test file that contains the D&M predicted parses rather than gold parses, 
then (2) providing this new test file to LISA and passing a command line flag which instructs LISA to predict 
using the provided parse information (rather than its own predicted parses, which is the default behavior).

To create a new test file, first [run the parser](#run-the-dmelmo-parser) with the test file for which you would like to predict parses.
If you ran the parser under `models/dm-conll05-elmo`, then there should be a new file generated: 
`models/dm-conll05-elmo/parse_preds.tsv`. Below we assume the original test file resides under the directory defined in
the environment variable `$CONLL05`. To create a new test file with parse heads and labels replaced with the predicted ones,
you can use the following script:
```bash
./bin/replace_gold_parse.sh $CONLL05/test.wsj.gz.parse.sdeps.combined.bio models/dm-conll05-elmo/parse_preds.tsv > test.wsj.gz.parse.sdeps.combined.bio.predicted
```

Now, you can run LISA evaluation using this test file instead of the original one, and tell LISA to use gold parses:
```bash
python network.py --load --test --test_eval --load_dir models/lisa-conll05 --config_file models/lisa-conll05/config.cfg --test_file test.wsj.gz.parse.sdeps.combined.bio.predicted --gold_attn_at_train False 
```

**Note that when you change the command line params (as above), `config.cfg` will be rewritten with the latest configuration settings. 
You can change this by specifying a directory to `--save_dir` which differs from `--load_dir`.**
(For simplicity, in all the above examples they are the same.)

Evaluate LISA using the gold parse
----
Similarly, you can easily evaluate LISA using the original, gold parses. To do so on the dev set only, omit the `--test_eval` flag:
```bash
python network.py --load --test --gold_attn_at_train False --load_dir models/lisa-conll05 --config_file models/lisa-conll05/config.cfg
```

Train a model:
----
We highly recommend using a GPU. 

To train a model with save directory `model` using the configuration file `lisa-conll05.conf`:
```bash
python network.py --config_file config/lisa-conll05.conf --save_dir model
```

Results
====

CoNLL-2005 results for released models (dev, WSJ test, Brown test):

| Model                       | P       | R       | F1      |     | P     | R     | F1    |     | P     | R     | F1    |
| --------------------------- | ------- | ------- | ------- | --- | ----- | ----- | ----- | --- | ----- | ----- | ----- |
| `sa-conll05`                | 83.52   | 81.28   | 82.39   |     | 84.17 | 83.28 | 83.72 |     | 72.98 | 70.10 | 71.51 |
| `lisa-conll05`              | 83.10   | 81.39   | 82.24   |     | 84.07 | 83.16 | 83.61 |     | 73.32 | 70.56 | 71.91 |
| `lisa-conll05` +D&M         | 84.44   | 82.89   | 83.66   |     | 85.98 | 84.85 | 85.41 |     | 75.93 | 73.45 | 74.67 |
| `lisa-conll05` *+Gold*      | *87.91* | *85.73* | *86.81* |     | ---   | ---   | ---   |     | ---   | ---   | ---   |
|||||||||
| `sa-conll05-elmo`           | 85.78   | 84.74   | 85.26   |     | 86.21 | 85.98 | 86.09 |     | 77.10 | 75.61 | 76.35 |
| `lisa-conll05-elmo`         | 86.07   | 84.64   | 85.35   |     | 86.69 | 86.42 | 86.55 |     | 78.95 | 77.17 | 78.05 |
| `lisa-conll05-elmo` +D&M    | 85.83   | 84.51   | 85.17   |     | 87.13 | 86.67 | 86.90 |     | 79.02 | 77.49 | 78.25 |
| `lisa-conll05-elmo` *+Gold* | *88.51* | *86.77* | *87.63* |     | ---   | ---   | ---   |     | ---   | ---   | ---   |


CoNLL-2012 results for released models (dev, test):

| Model                       | P       | R       | F1      |     | P     | R     | F1    |
| --------------------------- | ------- | ------- | ------- | --- | ----- | ----- | ----- |  
| `sa-conll12`                | 82.22   | 79.35   | 80.76   |     | 82.50 | 79.50 | 80.97 |
| `lisa-conll12`              | 81.70   | 79.28   | 80.47   |     | 81.69 | 78.96 | 80.30 |
| `lisa-conll12` +D&M         | 83.48   | 81.13   | 82.29   |     | 83.65 | 81.14 | 82.37 | 
| `lisa-conll12` +Gold        | 87.61   | 84.87   | 86.22   |     | ---   | ---   | ---   |
|||||||||
| `sa-conll12-elmo`           | 84.35   | 82.82   | 83.58   |     | 84.51 | 82.82 | 83.66 |
| `lisa-conll12-elmo`         | 84.52   | 82.98   | 83.75   |     | 84.45 | 82.86 | 83.65 |
| `lisa-conll12-elmo` +D&M    | 84.32   | 83.09   | 83.70   |     | 84.44 | 83.12 | 83.77 |
| `lisa-conll12-elmo` *+Gold* | *88.20* | *86.56* | *87.37* |     | ---   | ---   | ---   |