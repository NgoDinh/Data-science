#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 00:32:03 2017

@author: mmr
"""
import bs4
import sys
import requests


def get_result():
    df = requests.get('http://ketqua.net').text
    soup = bs4.BeautifulSoup(df, 'lxml')
    number_award = {0: 1, 1: 1, 2: 2, 3: 6, 4: 4, 5: 6, 6: 3, 7: 4}
    result = {}
    for number, value in number_award.items():
        temp = []
        for i in range(value):
            id_award = "rs_{}_{}".format(number, i)
            td = soup.findAll('td', {'id': id_award})
            temp.append(td[0].contents[0])
        result[number] = temp
    list_lo = []
    for number, value in result.items():
        for element in value:
            lo = element[-2:]
            if lo not in list_lo:
                list_lo.append(lo)
    return result, list_lo


def main():
    list_input = sys.argv[1:]
    result, list_lo = get_result()
    counter = 0
    for element in list_input:
        if str(element) in list_lo:
            print('You are so lucky with number: {}'.format(element))
            counter = counter + 1
    list_name = {0: "Dac Biet", 1: "Nhat", 2: "Nhi",
                 3: "Ba", 4: "Tu", 5: "Nam", 6: "Sau", 7: "Bay"}
    if counter == 0:
        for number, value in result.items():
            name = list_name[number]
            print('Giai {} la: {}'.format(name, '-'.join(value)))


if __name__ == "__main__":
    main()
