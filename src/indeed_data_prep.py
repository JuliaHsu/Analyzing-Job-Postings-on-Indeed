import json
import numpy as np
import pandas as pd
import os
import re
import glob
import csv

'''
* Data preprocessing for Indeed job posting dataset
'''

INDEED_JOB_POSTING_DATA = "/Users/julia/OneDrive - George Mason University/researchProject/4_JobPosting/data/"
CSV_DATA = '../data/'
def main():
    indeed_2020_df = read_json('Indeed_2020/')
    print(len(indeed_2020_df.columns.tolist()))
    indeed_preCovid_df = read_json('preCovid/')
    print(len(indeed_preCovid_df.columns.tolist()))

def read_json(dataset):
    data_dict = {}
    data_json = glob.glob( INDEED_JOB_POSTING_DATA + dataset + "*.json")
    indeed_df = pd.DataFrame()
    for i, json_file in enumerate(data_json):
        raw_df = pd.read_json(json_file,lines=True)
        data_dict[i] = raw_df
    lst_result = [values for values in data_dict.values()]
    indeed_df = indeed_df.append(lst_result)
    file_name = json_file.split('/')[-1]
    file_name = file_name.replace('.json','.csv')
    # indeed_df.to_csv(CSV_DATA + dataset +  file_name)
    return indeed_df

if __name__ == '__main__':
    main()