from django.conf.urls import url, include
from notebookSearchTest import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^genericsearch', views.genericsearch, name='genericsearch'), 
    url(r'^test', views.test, name='test')
]