from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import RepoDetails, Contributors
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from urllib.parse import urlsplit


def index(request):

    projects = RepoDetails.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'index.html', context)


def projects(request):

    projects = RepoDetails.objects.all()

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
    response_data = {}
    # projects = RepoDetails.objects.all()
    # for project in projects:
    #     if project.vcs_url and urlsplit(project.vcs_url).netloc == "github.com":
    #         response_data[project.project_name] = project.vcs_url
    #         url = "https://api.github.com/repos{0}?client_id={1}&client_secret={2}".format(urlsplit(project.vcs_url).path.split(".git")[0],
    #                                                                                        "80cfaecd567f874a3940",
    #                                                                                        "9e5228bd7f47f693058c422f22f915202cca3d45")
    #         response = requests.get(url)
    #         print("status:{0}, url:{1}".format(response.status_code, url))
    #         response = json.loads(response.text)
    #         response_data[project.project_name] = response.get("watchers_count")

    response_data = {
        "flutter-search-bar": 82,
        "ripgrep": 11316,
        "Sidekiq Queue Metrics": 8,
        "Homebrew-cask": 14101,
        "GoCD api client": 5,
        "Scientist4J": 224,
        "OpenMRS": 704,
        "appium-docker-android": 147,
        "Appium - Java client ": 0,
        "swtbot": 21,
        "Treadmill": 105,
        "DeviceManager": 13,
        "RemoteAppiumManager": 7,
        "Flips": 35,
        "reactivator": 0,
        "Tracker-enabled DbContext": 180,
        "Gauge": 1375,
        "Mart DHIS Sync": 0,
        "sim-boot": 0,
        "freeCodeCamp": 0,
        "MySController-rs": 10,
        "Rails distributed tracing": 2,
        "appium/java-client": 581,
        "AppiumTestDistribution": 526,
        "liquigraph": 82,
        "emacs-one-themes": 6,
        "go-langserver": 595,
        "nakal_java": 29,
        "Blockchain": 0,
        "pumba": 0,
        "wiremock": 2846,
        "pairing-matrix": 0,
        "OpenContacts": 0,
        "lambda-selenium": 7,
        "Kluent": 432,
        "serde_struct_wrapper": 2,
        "react-native-segmented-control-ui": 2,
        ".custom_commands": 1,
        "Socketcluster Java Client": 60,
        "gauge": 1375,
        "KubeGrid": 25,
        "data-anon": 8,
        "AssertjSwagger": 128,
        "Sherlock": 71,
        "Apache Gobblin": 1420,
        "awesome-appium": 165,
        "fake-smtp-server": 35,
        "CommandDotNet": 43,
        "redbaron": 323,
        "HTTParty": 4691,
        "appium": 8140,
        "spoon": 2475,
        "GoCD": 4460,
        "api_response_tester": 0,
        "taiko": 693,
        "Envoy-Pilot": 9,
        "apkToJava": 21,
        "Copious": 0,
        "Taiko": 693,
        "Pairing Matrix": 10,
        "jabba": 639
    }


    return Response(response_data)


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