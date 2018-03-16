#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 00:21:54 2017

@author: mmr
"""
import requests
import json


def count_page(n):
    number_page = n // 20
    last_page_results = n - (20 * number_page)
    return number_page, last_page_results


def get_result(file_key, n):
    number_page, last_page_results = count_page(n)
    myfile = open('google_key.json')
    google_key = json.load(myfile)['key']
    final_result = []
    link_base = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
                 'location=10.779614,106.699256&radius=5000&'
                 'hasNextPage=true&nextPage()=true&'
                 'keyword=coffee&key={}').format(google_key)
    for number in range(number_page):
        if number == 0:
            result, next_page_token = get_data(link_base, 20)
            final_result.extend(result)
        elif number == range(number_page)[-1]:
            if bool(next_page_token):
                link = link_base + '&pagetoken={}'.format(next_page_token)
                result, next_page_token = get_data(link, last_page_results)
                final_result.extend(result)
            else:
                break
        else:
            if bool(next_page_token):
                link = link_base + '&pagetoken={}'.format(next_page_token)
                result, next_page_token = get_data(link, 20)
                final_result.extend(result)
            else:
                break
    return final_result


def get_data(link, n):
    df = requests.get(link).text
    data_js = json.loads(df)
    try:
        next_page_token = data_js['next_page_token']
    except:
        next_page_token = None
    result = []
    for element in data_js['results'][:n]:
        temp = {}
        temp['name'] = element['name']
        temp['Address'] = element['vicinity']
        result.append(temp)
    return result, next_page_token


def main():
    result = get_result('google_key.json', 50)
    with open('hcm_coffee.json', 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    main()
