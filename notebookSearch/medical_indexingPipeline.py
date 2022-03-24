from django.forms.widgets import NullBooleanSelect, Widget
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import simplejson
from urllib.request import urlopen
import urllib
from datetime import datetime
from elasticsearch import Elasticsearch
from glob import glob
from elasticsearch_dsl import Search, Q, Index
from elasticsearch_dsl.query import MatchAll
from django.core import serializers
import numpy as np
import json
import uuid
import os
from github import BadCredentialsException, RateLimitExceededException 
from github import Github
import time
import re
ACCESS_TOKEN_Github= "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" # pathology crawler token in GitHub
ACCESS_TOKEN_Gitlab= "glpat-RLNz1MhmyeR7jcox_dyA"

# ----------------------------------------------------------------
def open_file(file):
    read_path = file
    with open(read_path, "r", errors='ignore') as read_file:
        data = json.load(read_file)
    return data
# ----------------------------------------------------------------
def indexingpipeline():
    es = Elasticsearch("http://localhost:9200")
    index = Index('notebooks', es)

    if not es.indices.exists(index='notebooks'):
        index.settings(
            index={'mapping': {'ignore_malformed': True}}
        )
        index.create()
    else:
        es.indices.close(index='notebooks')
        put = es.indices.put_settings(
            index='notebooks',
            body={
                "index": {
                    "mapping": {
                        "ignore_malformed": True
                    }
                }
            })
        es.indices.open(index='notebooks')
    cnt=0
    root=(os. getcwd()+"/Jupyter Notebook/")
    for path, subdirs, files in os.walk(root):
        for name in files:
            cnt=cnt+1
            indexfile= os.path.join(path, name)
            indexfile = open_file(indexfile)
            newRecord={
                "name":indexfile["name"],
                "full_name":indexfile["full_name"],
                "stargazers_count":indexfile["stargazers_count"],
                "forks_count":indexfile["forks_count"],
                "description":indexfile["description"],
                "size":indexfile["size"],
                "language": indexfile["language"],
                "html_url":indexfile["html_url"],
                "git_url":indexfile["git_url"]
            }
            res = es.index(index="notebooks", id= indexfile["git_url"], body=newRecord)
            es.indices.refresh(index="notebooks")
            print(str(cnt)+" recode added! \n")
# ----------------------------------------------------------------
def search_repository_github(keywords):
    g = Github(ACCESS_TOKEN_Github)
    keywords = [keyword.strip() for keyword in keywords.split(',')]
    keywords.append("notebook")
    query = '+'.join(keywords)+ '+in:readme+in:description'
    result = g.search_repositories(query, 'stars', 'desc')
    cnt=0
    data=[]
    iter_obj = iter(result)
    while True:
        try:
            cnt=cnt+1
            repo = next(iter_obj)
            new_record= {
                "id":cnt,
                "name": repo.full_name,
                "description": re.sub(r'[^A-Za-z0-9 ]+', '',repo.description),
                "html_url":repo.html_url,
                "git_url": repo.clone_url,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "size": repo.size,
            }


            if new_record["language"]=="Jupyter Notebook" and new_record not in data:
                data.append(new_record)
        except StopIteration:
            break
        except RateLimitExceededException:
            continue
    data=(json.dumps({"results_count": result.totalCount,"hits":data}).replace("'",'"'))
    return  json.loads(data)
# ----------------------------------------------------------------
def test():
    response_data=search_repository_github('')
    print(response_data)
    indexFile= open("notebooks.json","w+")
    indexFile.write(json.dumps(response_data))
    indexFile.close()
    indexingpipeline()
# ----------------------------------------------------------------

def get_most_starred_repos():
    g = Github(ACCESS_TOKEN_Github)
    languages=["Jupyter Notebook"]
    for lang in languages:
        i = 0
        # create folder named after current language
        if not os.path.exists(lang):
            os.makedirs(lang)
        # search top repos of lang by descending stars


        # Modify the below set of queries you will get returned notebooks from Github. (7-8 hours to crawer the Github)
        potentialQueries=[
            "breast", "cancer"]

        for query in potentialQueries:
            print ("\n\n------------------- Current query:  " + query.lower() +"  ---------------------\n\n")
            for repo in g.search_repositories(query.lower(),sort="stars", order="desc", language=lang):
                try:
                    temp_data = {}
                    temp_data["name"] = repo.name
                    temp_data["full_name"] = repo.full_name
                    temp_data["stargazers_count"] = repo.stargazers_count
                    temp_data["forks_count"] = repo.forks_count
                    temp_data["description"] = re.sub(r'[^A-Za-z0-9 ]+', '',repo.description)
                    temp_data["id"] = repo.id
                    temp_data["size"] = repo.size
                    temp_data["language"] = repo.language
                    temp_data["html_url"] = repo.html_url
                    temp_data["git_url"] = repo.clone_url
                    filename= re.sub(r'[^A-Za-z0-9 ]+', '',repo.name)+"_"+"_"+str(repo.id)+"_"+str(repo.size)
                    f = open(lang+"/"+filename+".json", 'w+')
                    f.write(json.dumps(temp_data))
                    f.close()
                    print(repo.html_url)
                except:
                    print("Pleaes wait for a couple of seconds...")
                    time.sleep(10)
            time.sleep(10)
# ----------------------------------------------------------------
indexingpipeline()
# test()
# get_most_starred_repos()