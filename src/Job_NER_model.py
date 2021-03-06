import numpy as np
import pandas as pd
import os
import re
import glob
import csv
import random
import spacy
from spacy.util import minibatch, compounding
from tqdm import tqdm, tqdm_notebook

ANN_DATA = '../data/ann_data/'
categories_dict = {'Indeed_NER_IT': 'internet','Indeed_NER_food': 'food', 'Indeed_NER_retail': 'retail', 'Indeed_NER_healthcare': 'healthcare' }

def ner_model(TRAIN_DATA, n_iter=500):
    print('Training started...')
    """Load the model, set up the pipeline and train the entity recognizer."""

    nlp = spacy.blank("en")  # create blank Language class
    print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        nlp.begin_training()
        for itn in tqdm_notebook(range(n_iter)):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
    print('Training completed.')
    return nlp


