#  Notebook search engine
A search engine for various types of research assets. 
Right now it is focused on notebook search. 
This is originally forked from `https://github.com/SiamakFarshidi/KMS-generic` 

## Project structure
From the infrastructure perspective : `Nginx` + `Gunicorn` + `Django` \
Nginx receives incoming requsts, passing through Gunicorn to Django


From the programming perspective: 
+ `HTML`, `CSS`, `JS` are used for constructing frontend UI
+ `Django` (mainly `setting.py` and `urls.py`) is used to handle requests that invoke Python functions



## Folder explanation
+ important configuration files
    - `opensemanticsearch/settings.py`: Django project global setting
    - `opensemanticsearch/settings.py`: URL configurations

+ `genericpages`: The main entry point of the search engine, containing a landing page

+ `notebookearch`: Notebook search module
+ `webSearch`: Web page searching module, including a crawler and a search engine
+ `DSS`: Crawler for datasets
    - `DSS/crawlerDatasetConfig.json`: Configuration file for the crawler. 

## Web page crawler
+ Configure the crawler: `webSearch/indexingPipeline/medicalwebsites.json`
+ Run the cralwer: 
```
cd webSearch/indexingPipeline
sudo python3 adhoc_crawler.py
```



## Development
A more detailed explanation for setting up environment: \
`https://docs.google.com/document/d/1icuUCTjaaa53uFE0tjAv1B3IyfzL57xqe2UeeCIXfEA/edit?usp=sharing`
+ When the search engine goes online, you can use Chrome inspection (F12) to inspect the frontend. 
+ `genericsearch` in the URL is projected to method `genericsearch()` that are defined in `views.py` under various modules. 

### Django interaction with fronten
+ `request()`: frontend --> Django
+ `render()`: Djano --> frontend

### Frontend design
+ https://codedthemes.com/item/category/templates/bootstrap-admin-templates/
+ Landingpage design: 