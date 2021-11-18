#!/usr/bin/env bash

VENVNAME=venv_twitter_sentiment

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate
pip install --upgrade pip


test -f requirements.txt && pip install -r requirements.txt

pip install -U pip setuptools wheel
#pip install -U spacy
python -m spacy download en_core_web_sm

cd data

unzip archive.zip

deactivate