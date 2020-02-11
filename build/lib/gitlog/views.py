from django.shortcuts import render
from django.http import HttpResponseRedirect
from .utils import getCommits
from .models import Commit
import os
# Create your views here.


def humanFormat(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def onlyYMD(datetime_object):
    return (datetime_object.year, datetime_object.month, datetime_object.day)


def index(request):
    commits = Commit.objects.all()
    formated_commits = []
    work_days = []
    line_of_code = 0
    for commit in commits:
        formated_commit = {}
        formated_commit['weekday'] = commit.datetime_object.strftime('%a')
        formated_commit['month'] = commit.datetime_object.strftime('%b')
        formated_commit['day'] = commit.datetime_object.strftime('%d')
        formated_commit['branch'] = commit.branch
        formated_commit['insertions_count'] = commit.insertions_count
        formated_commit['deletions_count'] = commit.deletions_count
        formated_commit['commit_note'] = commit.commit_note
        formated_commits.append(formated_commit)

        line_of_code += commit.insertions_count - commit.deletions_count
        if onlyYMD(commit.datetime_object) not in work_days:
            work_days.append(onlyYMD(commit.datetime_object))

    context = {
        'commits': formated_commits,
        'commits_count': len(formated_commits),
        'line_of_code': humanFormat(line_of_code),
        'days_of_work': len(work_days)

    }

    return render(request, 'gitlog/index.html', context)


def run(request):
    if request.method == 'POST':

        if os.getenv("THIS_ENV") == "development":
            commits = getCommits(production=False)
        else:
            commits = getCommits(production=True)


        for commit in commits:
            instance, created = Commit.objects.get_or_create(
                commit_hash=commit['commit_hash'],
                branch=commit['branch'],
                author=commit['author'],
                email=commit['email'],
                datetime_object=commit['datetime'],
                commit_note=commit['commit_note'],
                file_changed_count=commit['file_changed_count'],
                insertions_count=commit['insertions_count'],
                deletions_count=commit['deletions_count']
            )
            instance.save()

        commits_count = len(Commit.objects.all())
        message = "Create and Save. Got " + str(commits_count) + " Commits"
        commits = Commit.objects.all()
    else:
        commits = Commit.objects.all()
        commits_count = len(Commit.objects.all())
        message = 'wait to run, Got ' + str(commits_count) + " Commits"

    context = {
        'message': message,
        'commits': commits
    }
    return render(request, 'gitlog/run.html', context)
