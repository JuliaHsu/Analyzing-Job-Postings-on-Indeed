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
    # indeed_2020_df = read_json('Indeed_2020/')
    # print(len(indeed_2020_df.columns.tolist()))
    indeed_preCovid_df = read_json('preCovid/')
    print(len(indeed_preCovid_df.columns.tolist()))

def read_json(dataset):
    data_dict = {}
    data_json = glob.glob( INDEED_JOB_POSTING_DATA + dataset + "*.json")
    indeed_df = pd.DataFrame()
    csv_name = ''
    for i, json_file in enumerate(data_json):
        print(json_file)
        raw_df = pd.read_json(json_file,lines=True)
        data_dict[i] = raw_df
        file_name = json_file.split('/')[-1]
        file_name = file_name.replace('.json','')
        csv_name = csv_name + "_" + file_name
    lst_result = [values for values in data_dict.values()]
    indeed_df = indeed_df.append(lst_result)
    date1 = csv_name.split('_')[1] 
    print(date1)
    date2 = csv_name.split('_')[-1] 
    indeed_df.to_csv(CSV_DATA + dataset +  date1 + "_" + date2 +  ".csv") 
    return indeed_df

if __name__ == '__main__':
    main()