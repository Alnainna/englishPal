from WordFreq import WordFreq
from wordfreqCMD import youdao_link, sort_in_descending_order
import pickle_idea, pickle_idea2
import os
import random, glob
import hashlib
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for, session, abort, flash, get_flashed_messages
from difficulty import get_difficulty_level_for_user, text_difficulty_level, user_difficulty_level
from model.article import get_all_articles, get_article_by_id, get_number_of_articles
import logging

path_prefix = './'
db_path_prefix = './db/'  # comment this line in deployment


def total_number_of_essays():
    return get_number_of_articles()


def get_article_title(s):
    return s.split('\n')[0]


def get_article_body(s):
    lst = s.split('\n')
    lst.pop(0)  # remove the first line
    return '\n'.join(lst)


def get_today_article(user_word_list, visited_articles):
    if visited_articles is None:
        visited_articles = {
            "index" : 0,  # 为 article_ids 的索引
            "article_ids": []  # 之前显示文章的id列表，越后越新
        }
    if visited_articles["index"] > len(visited_articles["article_ids"])-1:  # 生成新的文章，因此查找所有的文章
        result = get_all_articles()
    else:  # 生成阅读过的文章，因此查询指定 article_id 的文章
        if visited_articles["article_ids"][visited_articles["index"]] == 'null':  # 可能因为直接刷新页面导致直接去查询了'null'，因此当刷新的页面的时候，需要直接进行“上一篇”操作
            visited_articles["index"] -= 1
            visited_articles["article_ids"].pop()
        article_id = visited_articles["article_ids"][visited_articles["index"]]
        result = get_article_by_id(article_id)
    random.shuffle(result)

    # Choose article according to reader's level
    logging.debug('* get_today_article(): start d1 = ... ')
    d1 = load_freq_history(user_word_list)
    d2 = load_freq_history(path_prefix + 'static/words_and_tests.p')
    logging.debug(' ... get_today_article(): get_difficulty_level_for_user() start')
    d3 = get_difficulty_level_for_user(d1, d2)
    logging.debug(' ... get_today_article(): done')

    d = None
    result_of_generate_article = "not found"

    d_user = load_freq_history(user_word_list)
    logging.debug('* get_today_article(): user_difficulty_level() start')
    user_level = user_difficulty_level(d_user, d3)  # more consideration as user's behaviour is dynamic. Time factor should be considered.
    logging.debug('* get_today_article(): done')
    text_level = 0
    if visited_articles["index"] > len(visited_articles["article_ids"])-1:  # 生成新的文章
        amount_of_visited_articles = len(visited_articles["article_ids"])
        amount_of_existing_articles = result.__len__()
        if amount_of_visited_articles == amount_of_existing_articles:  # 如果当前阅读过的文章的数量 == 存在的文章的数量，即所有的书本都阅读过了
            result_of_generate_article = "had read all articles"
        else:
            for k in range(3):  # 最多尝试3次
                for reading in result:
                    text_level = text_difficulty_level(reading['text'], d3)
                    factor = random.gauss(0.8, 0.1)  # a number drawn from Gaussian distribution with a mean of 0.8 and a stand deviation of 1
                    if reading['article_id'] not in visited_articles["article_ids"] and within_range(text_level, user_level, (8.0 - user_level) * factor):  # 新的文章之前没有出现过且符合一定范围的水平
                        d = reading
                        visited_articles["article_ids"].append(d['article_id'])  # 列表添加新的文章id；下面进行
                        result_of_generate_article = "found"
                        break
                if result_of_generate_article == "found":  # 用于成功找到文章后及时退出外层循环
                    break
        if result_of_generate_article != "found":  # 阅读完所有文章，或者循环3次没有找到适合的文章，则放入空（“null”）
            visited_articles["article_ids"].append('null')
    else:  # 生成已经阅读过的文章
        d = random.choice(result)
        text_level = text_difficulty_level(d['text'], d3)
        result_of_generate_article = "found"

    today_article = None
    if d:
        today_article = {
            "user_level": '%4.1f' % user_level,
            "text_level": '%4.1f' % text_level,
            "date": d['date'],
            "article_title": get_article_title(d['text']),
            "article_body": get_article_body(d['text']),
            "source": d["source"],
            "question": get_question_part(d['question']),
            "answer": get_answer_part(d['question'])
        }

    return visited_articles, today_article, result_of_generate_article


def load_freq_history(path):
    d = {}
    if os.path.exists(path):
        d = pickle_idea.load_record(path)
    return d


def within_range(x, y, r):
    return x > y and abs(x - y) <= r


def get_question_part(s):
    s = s.strip()
    result = []
    flag = 0
    for line in s.split('\n'):
        line = line.strip()
        if line == 'QUESTION':
            result.append(line)
            flag = 1
        elif line == 'ANSWER':
            flag = 0
        elif flag == 1:
            result.append(line)
    return '\n'.join(result)


def get_answer_part(s):
    s = s.strip()
    result = []
    flag = 0
    for line in s.split('\n'):
        line = line.strip()
        if line == 'ANSWER':
            flag = 1
        elif flag == 1:
            result.append(line)
    return '\n'.join(result)
