"""Generate Github issues for entrypoints defined in setup.cfg
"""
import os
import time
import random
import tapis_cli
from github import Github

PROJECT = 'mwvaughn/tapis-cli'
LABEL_PREFIX = 'service.'

gh = Github(os.environ.get('GITHUB_API_KEY').strip())
repo = gh.get_repo(PROJECT)

issues_raw = repo.get_issues(state='all')
issue_titles = [u.title for u in issues_raw]

for cmd in tapis_cli.utils.command_set():
    path_els = cmd.split(' ')
    api = path_els[0]
    label = '{0}{1}'.format(LABEL_PREFIX, api)
    title = 'Implement: {0}'.format(cmd)
    if title not in issue_titles:
        print('Creating issue "{0}"...'.format(title))
        issue_body = {
            'title': title,
            'body': 'Add a "{0}" command to tapis-cli'.format(cmd),
            'labels': [label]
        }
        repo.create_issue(**issue_body)
        print('Created')
        # Stagger API calls a little bit
        time.sleep(random.random() * 3)
    else:
        print('Issue exists - {0}'.format(title))
