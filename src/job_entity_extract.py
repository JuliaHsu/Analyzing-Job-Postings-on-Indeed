import json
import numpy as np
import pandas as pd
import re
import glob
import spacy
from spacy.util import minibatch, compounding
import Job_NER_model
import itertools

ANN_DATA = '../data/ann_data/'
PROCESSED_DATA = '../data/processed_data/'
SAMPLED_DATA = PROCESSED_DATA + 'random_sample/'

categories_dict = {'Indeed_NER_IT': 'internet','Indeed_NER_food': 'food', 'Indeed_NER_retail': 'retail', 'Indeed_NER_healthcare': 'healthcare' }



def main():
    # read_ann_json()

    # ner_train = []
    # for cat in categories_dict.keys():
    #     with open(ANN_DATA + cat + "/" + cat + "_ann.txt","r") as f:
    #         print(f)
    #         for line in f.readlines():
    #             ner_train.append(eval(line))
    #     train_ner_ml(ner_train, cat.split('_')[-1])

    ner_pred('2019', '20190501_20190630_IT.csv', 'IT')
    ner_pred('2020', '20200501_20200630_IT.csv', 'IT')

    # ner_pred('2019', '20190501_20190630_healthcare.csv', 'healthcare')
    # ner_pred('2020', '20200501_20200630_healthcare.csv', 'healthcare')

    # ner_pred('2019', '20190501_20190630_food.csv', 'food')
    # ner_pred('2020', '20200501_20200630_food.csv', 'food')

    # ner_pred('2019', '20190501_20190630_retail.csv', 'retail')
    # ner_pred('2020', '20200501_20200630_retail.csv', 'retail')

def read_ann_json():
    for cat in categories_dict.keys():
        jsons = glob.glob(ANN_DATA + cat + '/*/*.ann.json')
        legend_json = ANN_DATA + cat + '/annotations-legend.json'
        cat_job_ner_ls = []
        try:
            ann_legends = open(legend_json)
            legend_dict = json.load(ann_legends)
        except IOError:
            print(legend_json + "not accessible")
        for ann_json in jsons:
            with open(ann_json) as json_data:
                data = json.load(json_data)
                job_id = ann_json.split('/')[-1]
                job_id = job_id.split('_')[-1]
                job_id = job_id.replace('.txt.ann.json','')
                if ann_json.split('/')[4] == '2019':
                    job_desc = get_job_desc('2019_' + job_id, cat)
                else:
                    job_desc = get_job_desc(job_id,cat)
                entities = data['entities']
                format_entities = []
                entities_dict = {}
                for entity in entities:
                    entity_id = entity['classId']
                    entity_name = legend_dict[entity_id]
                    start_offset = entity['offsets'][0]['start'] #start
                    entity_text = entity['offsets'][0]['text']
                    end_offset = len(entity_text) + start_offset
                    entity_tup = (start_offset, end_offset, entity_name)
                    format_entities.append(entity_tup)
                entities_dict['entities'] = format_entities
                job_ner_tup = (job_desc, entities_dict)
                all_ann_txt = open(ANN_DATA + cat + '/' + cat + "_ann.txt", "a")
                all_ann_txt.write(str(job_ner_tup) + "\n")
                all_ann_txt.close()
        
def get_job_desc(job_id,cat):
    f = open(SAMPLED_DATA + categories_dict[cat] + "/" + categories_dict[cat] + "_" + job_id + ".txt", "r")
    job_desc = f.read()
    return job_desc

def train_ner_ml(TRAIN_DATA, cat):
    job_ner_model = Job_NER_model.ner_model(TRAIN_DATA)
    job_ner_model.to_disk('model/' + cat + "_ner_model")
    return job_ner_model

def ner_pred(year, job_csv, cat):
    ner_model = spacy.load('model/' + cat + "_ner_model")
    # job_df = pd.read_csv(PROCESSED_DATA + '2020/'+'20200501_20200630_computer_internet.csv', index_col=0)
    job_df = pd.read_csv(PROCESSED_DATA + year + '/' + job_csv, index_col=0)
    job_df.reset_index(drop = True, inplace = True)
   
    job_df['temp_entity'] = job_df['job_description'].apply(lambda x: _ner_apply(ner_model, x))
    job_df = job_df[['uniq_id','job_title','category','company_name','city','state','job_description','temp_entity']]

    job_df = format_entities_df(job_df)
    job_df.to_csv('../result/' + cat + '_job_entity_' + year + '.csv')
def _ner_apply(ner_model, text):
    # pass our text to spacy
    # it will return us doc (spacy doc)
    doc = ner_model(text)
    # return list of tuples look like 
    # this [('four-year', 'EDUCATION_YEARS'), ('college or university', 'SCHOOL_TYPE')]
    return [(ent.text, ent.label_) for ent in doc.ents]

def format_entities_df(df_jobs):
    flatter = sorted( [ list(x) + [idx] for idx, y in enumerate(df_jobs['temp_entity']) for x in y], key = lambda x: x[1]) 
    # Find all of the values that will eventually go in each F column                
    for key, group in itertools.groupby(flatter, lambda x: x[1]):
        list_of_vals = [(val, idx) for val, _, idx in group]
        df_jobs[key] = [[] for i in range(df_jobs.shape[0]) ]
        # Add each value at the appropriate index and F column
        for val, idx in list_of_vals:
            df_jobs.loc[idx, key].append(val) 
        df_jobs[key] = df_jobs[key].apply(lambda x: list(set(x)))
        
            
    return df_jobs

if __name__ == '__main__':
    main()