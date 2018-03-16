# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import json
import sys


def get_data(n, tag):
    link = 'https://api.stackexchange.com'
    path = ('/2.2/questions?pagesize={}&order=desc&'
            'sort=votes&tagged={}&site=stackoverflow').format(n, tag)
    df = requests.get(link + path).text
    data_js = json.loads(df)
    for ques in data_js['items']:
        print(ques['title'])
        link_so = ques['link']
        ques_id = ques['question_id']
        # Use question{ID} API to find the most voted answer
        ques_path = ('/2.2/questions/{}/answers?order=desc&sort=votes&'
                     'site=stackoverflow').format(ques_id)
        ques_df = requests.get(link + ques_path).text
        ques_js = json.loads(ques_df)
        best_ans = ques_js['items'][0]
        ans_id = best_ans['answer_id']
        # create best answer link by answer ID
        ans_link = link_so + "/{}#{}".format(ans_id, ans_id)
        print(ans_link)
        print('-' * 10)


def main():
    n = sys.argv[1]
    tag = sys.argv[2]
    get_data(n, tag)


if __name__ == "__main__":
    main()
