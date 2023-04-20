#!/bin/bash

pip3 install -q beautifulsoup4 pandas numpy IPython requests datetime flask nltk pymorphy2 joblib==1.1.0 hdbscan tqdm sklearn

python3 ./routes.py
