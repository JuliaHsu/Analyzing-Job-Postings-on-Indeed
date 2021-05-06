### How COVID-19 affects labor demands in the USA by analyzing Job Postings on Indeed.com
* AIT 664 Final Project (Spring 2021)
* Authors: Julia Hsu, Aiswarya Kannan & Hiba Siraj

### Procedure:
1. Data Preparation & Preprocessing:
* [raw_data_stat.ipynb](https://github.com/JuliaHsu/Analyzing-Job-Postings-on-Indeed/blob/master/src/raw_data_stat.ipynb): convert json files to csv format and get exploare the raw dataset
* [indeed_data_prep.py](https://github.com/JuliaHsu/Analyzing-Job-Postings-on-Indeed/blob/master/src/indeed_data_prep.py): randomly sample 400 job postings for annotation

2. Custom NER model for job description:
* [Job_NER_model.py](https://github.com/JuliaHsu/Analyzing-Job-Postings-on-Indeed/blob/master/src/Job_NER_model.py): Custom NER model
* [job_entity_extract](https://github.com/JuliaHsu/Analyzing-Job-Postings-on-Indeed/blob/master/src/job_entity_extract.py): extract entities from job description
