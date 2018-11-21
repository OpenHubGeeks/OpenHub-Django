from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='user'),
    url(r'^allprojects/$', views.projects, name='projects'),
    url(r'^api/techstack-data/$', views.get_techstack_count, name='api-data'),
    url(r'^api/office-dist-data/$', views.OfficeDistribution.as_view()),
    url(r'^api/git-stats/$', views.get_github_stats, name='git-data')
]
