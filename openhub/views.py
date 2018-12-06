from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import RepoDetails, Contributors
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from urllib.parse import urlsplit
from django.db.models import Q
import grequests


def index(request):

    projects = RepoDetails.objects.all()
    projects_count = RepoDetails.objects.values('contributor','contributor__user_firstname', 'contributor__user_photo').annotate(total=Count('contributor')).order_by('-total')[:5]
    context = {
        'projects': projects,
        'contributors': projects_count
    }

    print(context.get("contributors"))

    return render(request, 'index.html', context)


def projects(request):

    query = request.GET.get('q')
    if query is None:
        projects = RepoDetails.objects.all()
    else:
        projects = RepoDetails.objects.filter(Q(project_name__icontains=query) | Q(project_description__icontains=query) | Q(project_techstack__icontains=query))

    context = {
        'projects': projects
    }
    return render(request, 'projects.html', context)


@api_view(['GET'])
def get_techstack_count(request):
    column_name = 'project_techstack'
    projects = RepoDetails.objects.values(column_name).order_by(column_name).annotate(total=Count(column_name)).exclude(project_techstack__exact='NA')
    response = projects
    return Response(response)


@api_view(['GET'])
def get_github_stats(request):
    star_count = {}
    issues_count = {}
    forks_count = {}
    projects = RepoDetails.objects.all()
    url_list = []
    project_list = []
    for project in projects:
        if project.vcs_url and urlsplit(project.vcs_url).netloc == "github.com":
            url = "https://api.github.com/repos{0}?client_id={1}&client_secret={2}".format(urlsplit(project.vcs_url).path.split(".git")[0],
                                                                                           "80cfaecd567f874a3940",
                                                                                           "9e5228bd7f47f693058c422f22f915202cca3d45")
            url_list.append(url)
            project_list.append(project.project_name)

    rs = (grequests.get(u) for u in url_list)
    responses = grequests.map(rs)

    for i in range(len(responses)):
        response = json.loads(responses[i].text)
        star_count[project_list[i]] = response.get("watchers_count")
        issues_count[project_list[i]] = response.get("open_issues_count")
        forks_count[project_list[i]] = response.get("forks_count")

    response_data = {"stars": star_count, "issues": issues_count, "forks": forks_count}

    query = request.GET.get('count')

    response_star_list = []
    response_issues_list = []
    response_forks_list = []

    for key, value in sorted(response_data.get("stars").items(), key=lambda x: x[1], reverse=True)[:int(query)]:
        response_star_list.append([key, value])

    for key, value in sorted(response_data.get("issues").items(), key=lambda x: x[1], reverse=True)[:int(query)]:
        response_issues_list.append([key, value])

    for key, value in sorted(response_data.get("forks").items(), key=lambda x: x[1], reverse=True)[:int(query)]:
        response_forks_list.append([key, value])


    final_response_dict = {
        "top_stars": response_star_list,
        "top_issues": response_issues_list,
        "top_forks": response_forks_list
    }

    return Response(final_response_dict)


class OfficeDistribution(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            contributors = Contributors.objects.all().values('office').annotate(total=Count('office'))
            response = []
            for entry in contributors:
                response.append({'office': entry['office'], 'count': entry['total']})
        except:
            response = json.dumps([{'Error': 'No such office'}])
        return Response(response)