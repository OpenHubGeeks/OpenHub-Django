from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='openhub'),
    url(r'^allprojects/$', views.projects, name='projects'),
    url(r'^api/techstack-data/$', views.get_techstack_count, name='api-data'),
    url(r'^api/office-dist-data/$', views.OfficeDistribution.as_view()),
    url(r'^api/get-stars/$', views.fetch_stars, name='indi-stars'),
    url(r'^api/get-issues/$', views.fetch_issues, name='indi-issues'),
    url(r'^api/get-forks/$', views.fetch_forks, name='indi-forks'),
    url(r'^users/(?P<user_id>\d+)/$', views.users, name='user')
]