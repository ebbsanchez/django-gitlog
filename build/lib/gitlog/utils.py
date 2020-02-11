###
# inspired by https://gist.github.com/simonw/091b765a071d1558464371042db3b959
###

import subprocess
import datetime
import os


def getCommits(production=False):
    raw_text = getGitLog(production)
    commits = gitLogToList(raw_text)
    constructred_commits = []
    for commit_dict in commits:
        constructred_commit_dict = constructForDB(commit_dict)
        constructred_commits.append(constructred_commit_dict)
    # saveCommitToDB(constructred_commit_dict, model)
    return constructred_commits


def getGitLog(production):
    if not production:
        raw = subprocess.check_output(
            ['git', 'log', '--branches', '--decorate', '--shortstat'],
            stderr=subprocess.STDOUT
        ).decode("utf-8")
        saveLog(raw)
    else:
        raw = readLog()
    return raw


def saveLog(raw):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'gitlog.txt')
    with open(file_path, 'w') as f:
        raw = f.write(raw)
    return


def readLog():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'gitlog.txt')
    with open(file_path, 'r') as f:
        raw = f.read()
    return raw


def gitLogToList(raw_text):
    commits = []
    current_commit = {}
    lines = raw_text.split("\n")
    for line in lines:
        if line == '':
            continue
        if line.startswith('commit '):
            if current_commit:
                commits.append(current_commit)
                current_commit = {}
            commit_hash, branch = parseCommitLine(line)
            current_commit['commit_hash'] = commit_hash
            current_commit['branch'] = branch
        elif line.startswith('  '):
            commit_note = line.strip()
            current_commit["commit_note"] = commit_note
        elif line.startswith(' '):
            current_commit['stat'] = line.strip()
        else:
            key, value = line.split(':', 1)
            current_commit[key.lower()] = value.strip()
    # Save the last commit
    commits.append(current_commit)
    return commits


def parseCommitLine(line):
    _, commit_hash = line[:47].split(' ')
    if '(' in line:
        branch = line[48:][1:-1]
    else:
        branch = 'master'
    return commit_hash, branch


def constructForDB(commit):
    constructred_dict = {}

    # commit_hash  40 char
    constructred_dict['commit_hash'] = commit['commit_hash']
    # branch 30 char
    constructred_dict['branch'] = commit['branch']

    # Author 30 char # Mail 30 char
    author, email = commit['author'].split('<')
    constructred_dict['author'] = author.strip()
    constructred_dict['email'] = email[-1].strip()

    # Date timestamp
    datetime_object = datetime.datetime.strptime(
        commit['date'], '%a %b %d %H:%M:%S %Y %z')
    constructred_dict['datetime'] = datetime_object

    # Commit_note  200 char
    constructred_dict['commit_note'] = commit['commit_note']

    # file_changed_count int # insertions_count int # deletions_count int
    try:
        file_changed_count, insertions_count, deletions_count = parseStatLine(
            commit['stat'])
    except KeyError:
        if commit['merge']:
            file_changed_count, insertions_count, deletions_count = (0, 0, 0)
        else:
            raise KeyError

    constructred_dict['file_changed_count'] = file_changed_count
    constructred_dict['insertions_count'] = insertions_count
    constructred_dict['deletions_count'] = deletions_count

    return constructred_dict


def parseStatLine(statLine):

    stats = statLine.split(',')
    file_changed_count = 0
    insertions_count = 0
    deletions_count = 0

    for stat in stats:
        if 'changed' in stat:
            file_changed_count = int(stat.strip().split(' ')[0])
        elif 'insertion' in stat:
            insertions_count = int(stat.strip().split(' ')[0])
        elif 'deletion' in stat:
            deletions_count = int(stat.strip().split(' ')[0])
    return (file_changed_count, insertions_count, deletions_count)


# def saveCommitToDB(constructred_commit):
#     instance = MyModel(
#         commit_hash=constructred_dict['commit_hash'],
#         branch=constructred_dict['branch'],
#         author=constructred_dict['author'],
#         email=constructred_dict['email'],
#         datetime_object=constructred_dict['datetime'],
#         commit_note=constructred_dict['commit_note'],
#         file_changed_count=constructred_dict['file_changed_count'],
#         insertions_count=constructred_dict['insertions_count'],
#         deletions_count=constructred_dict['deletions_count']
#     )
#     instance.save()
