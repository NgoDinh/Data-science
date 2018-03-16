#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 00:18:49 2017

@author: vu.ngo
"""
import requests
import json
import sys


def get_data(user_name):
    len_name = len(user_name)
    link = 'https://api.github.com/users/{}/repos'.format(user_name)
    json_data = requests.get(link).text
    data_dict = json.loads(json_data)
    list_repos = []
    for element in data_dict:
        repos_link = element['issues_url']
        start = repos_link.find(user_name) + len_name + 1
        end = repos_link.find('/', start)
        repos = repos_link[start:end]
        list_repos.append(repos)
    return list_repos


def main():
    user_name = sys.argv[1]
    try:
        print(get_data(user_name))
    except:
        print("We can't find your input user_name at github")


if __name__ == "__main__":
    main()
