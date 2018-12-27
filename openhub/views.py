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
    projects_count = RepoDetails.objects.values('contributor', 'contributor__cid', 'contributor__user_firstname', 'contributor__user_photo').annotate(total=Count('contributor')).order_by('-total')[:5]
    context = {
        'projects': projects,
        'contributors': projects_count
    }

    return render(request, 'index.html', context)


def projects(request):

    query = request.GET.get('q')
    if query is None:
        projects = RepoDetails.objects.all().order_by('-total_stars')
    else:
        projects = RepoDetails.objects.filter(Q(project_name__icontains=query) | Q(project_description__icontains=query) | Q(project_techstack__icontains=query) | Q(contributor__cid__icontains=query)).order_by('-total_stars')

    context = {
        'projects': projects,
    }
    return render(request, 'projects.html', context)


@api_view(['GET'])
def get_techstack_count(request):
    column_name = 'project_techstack'
    projects = RepoDetails.objects.values(column_name).order_by(column_name).annotate(total=Count(column_name)).exclude(project_techstack__exact='NA')
    response = projects
    return Response(response)


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


@api_view(['GET'])
def fetch_stars(request):
    projects = RepoDetails.objects.values('project_name', 'total_stars').order_by('-total_stars')[:5]
    response = projects
    return Response(response)


@api_view(['GET'])
def fetch_issues(request):
    projects = RepoDetails.objects.values('project_name', 'total_issues').order_by('-total_issues')[:5]
    response = projects
    return Response(response)


@api_view(['GET'])
def fetch_forks(request):
    projects = RepoDetails.objects.values('project_name', 'total_forks').order_by('-total_forks')[:5]
    response = projects
    return Response(response)


@api_view(['GET'])
def users(request, user_id):
    contributor = Contributors.objects.get(pk=user_id)
    projects = RepoDetails.objects.filter(contributor__cid=user_id)
    print (projects)
    context = {
        'contributor': contributor,
        'projects': projects
    }
    return render(request, 'user.html', context=context)