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
PROCESSED_DATA = '../data/processed_data/'
def main():
    get_rand_job_desc('2019')
    

def get_rand_job_desc(year):
    print(PROCESSED_DATA + year)
    processed_files = glob.glob(PROCESSED_DATA + year + "/*.csv")
    print(processed_files)

    for f in processed_files:
        job_df = pd.read_csv(f, index_col=0)
        job_df = job_df[['uniq_id','job_description']]
        job_df = job_df.sample(n = 50)
        f = f.split('/')[-1]
        
        category = f.split('_')[-1]
        category = category.replace('.csv','')
        job_df.reset_index(drop = True, inplace = True)
        for row in range(job_df.shape[0]):
            desc = job_df.at[row,'job_description']
            job_id = job_df.at[row,'uniq_id']
            if category == "IT":
                category = "internet"
            f = open(PROCESSED_DATA + category + "/" + category + "_" + year + "_" + job_id + ".txt", "w")
            f.write(desc)
            f.close()
        # job_df.to_csv(PROCESSED_DATA + category + ".csv")

if __name__ == '__main__':
    main()