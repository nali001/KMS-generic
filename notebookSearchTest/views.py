from django.shortcuts import render
from django.http import HttpResponse
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
import requests
from bs4 import BeautifulSoup
from spellchecker import SpellChecker

# Create your views here.

def genericsearch(request): 
    # return HttpResponse('Hi, are you looking for notebooks?')
    return render(request,'notebook_results_test.html',{} )

def test(request): 
    # return HttpResponse('Hi, are you looking for notebooks?')
    result = {'operation': 'add', 'result': '20'} 
    return render(request,'notebook_results_test.html', result)
