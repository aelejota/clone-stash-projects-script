#!/usr/bin/env python
# -*- coding: utf_8 -*-

"""Module name
Script to clone all the repos under a Stash/Bitbucket project in local
"""
__author__  = 'jotaele'
__contact__ = 'antonjuanluis@gmail.com'
__version__ = '0.1'

# Modules
import sys
import os
import time
import stashy

# Main program
if __name__ == '__main__':

    USER = '<USER>'
    PASSWORD = '<PASSWORD>'
    STASH_URL = '<STASH_URL>'
    GIT_DIR = '<GIT_DIR>'

    l = []

    stash = stashy.connect(STASH_URL, USER, PASSWORD)
    for p in stash.projects.list():
        d = { k: p[k] for k in ['name', 'key'] }
        l.append(d)

    while True:
        for a, b in enumerate([e['name'] for e in l], 1):
            print('{} - {}'.format(a, b))

        answer = input('Please choose one Project: ')
        try:
            i = int(answer)
            if i < 1 or i > len(l):
                print('\nSorry, input must be between 1 to {}'.format(len(l)))
                time.sleep(2)
                continue
            break
        except ValueError:
            print("That's not an a valid number!")

    proj = l[i - 1]

    answer2 = ""
    while answer2 not in ['y', 'n']:
        answer2 = raw_input('Clone all repos of ' + proj['name'] + ' project?: (Y/N)').lower()
    if answer2 == "n":
        sys.exit(0)


    try:
        os.chdir(os.path.expanduser(GIT_DIR))
        if not os.path.isdir(proj['name']):
            os.makedirs(proj['name'])
            print("Creating: ", proj['name'])
        os.chdir(proj['name'])
    except Exception as exc:
        print(exc)
        sys.exit(1)

    for repo in stash.projects[proj['key']].repos.list():
        for url in repo["links"]["clone"]:
            if url["name"] == "ssh":
                if not os.path.isdir(repo['slug']):
                    os.system("git clone %s" % url['href'])
                else:
                    print("Pulling %s" % repo['slug'])
                    os.system("git -C %s pull" % repo['slug'])
                print("---")
    sys.exit(0)
