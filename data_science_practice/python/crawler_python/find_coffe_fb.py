# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import json
import requests


def build_url(token_file):
    my_file = open(token_file)
    my_token = json.load(my_file)
    url = ('https://graph.facebook.com/search?'
           'q=coffee&tea&cafe&caphe&trada&'
           'type=place&center=21.027875,105.853654&'
           'distance=1000&fields=location,website,name&'
           'access_token={}|{}'
           .format(my_token['Facebook App ID'], my_token['FaceApp Secret']))
    return(url)


def get_data(url):
    resp = requests.get(url).text
    mydata = json.loads(resp)
    return mydata['data']


def main():
    result = get_data((build_url('token.json')))
    with open('hanoi_coffee.json', 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    main()
