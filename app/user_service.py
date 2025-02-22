from datetime import datetime
from admin_service import ADMIN_NAME
from flask import *

# from app import Yaml
# from app.Article import get_today_article, load_freq_history
# from app.WordFreq import WordFreq
# from app.wordfreqCMD import sort_in_descending_order

import Yaml
from Article import get_today_article, load_freq_history
from WordFreq import WordFreq
from wordfreqCMD import sort_in_descending_order

import pickle_idea
import pickle_idea2

import logging
logging.basicConfig(filename='log.txt', format='%(asctime)s %(message)s', level=logging.DEBUG)

# 初始化蓝图
userService = Blueprint("user_bp", __name__)

path_prefix = '/var/www/wordfreq/wordfreq/'
path_prefix = './'  # comment this line in deployment

@userService.route("/get_next_article/<username>",methods=['GET','POST'])
def get_next_article(username):
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    session['old_articleID'] = session.get('articleID')
    if request.method == 'GET':
        visited_articles = session.get("visited_articles")
        if visited_articles['article_ids'][-1] == "null":  # 如果当前还是“null”，则将“null”pop出来,无需index+=1
            visited_articles['article_ids'].pop()
        else:  # 当前不为“null”，直接 index+=1
            visited_articles["index"] += 1
        session["visited_articles"] = visited_articles
        logging.debug('/get_next_article: start calling get_today_arcile()')
        visited_articles, today_article, result_of_generate_article = get_today_article(user_freq_record, session.get('visited_articles'))
        logging.debug('/get_next_arcile: done.')
        data = {
            'visited_articles': visited_articles,
            'today_article': today_article,
            'result_of_generate_article': result_of_generate_article
        }
    else:
        return 'Under construction'
    return json.dumps(data)

@userService.route("/get_pre_article/<username>",methods=['GET'])
def get_pre_article(username):
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    if request.method == 'GET':
        visited_articles = session.get("visited_articles")
        if(visited_articles["index"]==0):
            data=''
        else:
            visited_articles["index"] -= 1  # 上一篇，index-=1
            if visited_articles['article_ids'][-1] == "null":  # 如果当前还是“null”，则将“null”pop出来
                visited_articles['article_ids'].pop()
            session["visited_articles"] = visited_articles
            visited_articles, today_article, result_of_generate_article = get_today_article(user_freq_record, session.get('visited_articles'))
            data = {
                'visited_articles': visited_articles,
                'today_article': today_article,
                'result_of_generate_article':result_of_generate_article
            }
        return json.dumps(data)

@userService.route("/<username>/<word>/unfamiliar", methods=['GET', 'POST'])
def unfamiliar(username, word):
    '''

    :param username:
    :param word:
    :return:
    '''
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea.unfamiliar(user_freq_record, word)
    session['thisWord'] = word  # 1. put a word into session
    session['time'] = 1
    return "success"


@userService.route("/<username>/<word>/familiar", methods=['GET', 'POST'])
def familiar(username, word):
    '''

    :param username:
    :param word:
    :return:
    '''
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea.familiar(user_freq_record, word)
    session['thisWord'] = word  # 1. put a word into session
    session['time'] = 1
    return "success"


@userService.route("/<username>/<word>/del", methods=['GET', 'POST'])
def deleteword(username, word):
    '''
    删除单词
    :param username: 用户名
    :param word: 单词
    :return: 重定位到用户界面
    '''
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    pickle_idea2.deleteRecord(user_freq_record, word)
    # 模板userpage_get.html中删除单词是异步执行，而flash的信息后续是同步执行的，所以注释这段代码；同时如果这里使用flash但不提取信息，则会影响 signup.html的显示。bug复现：删除单词后，点击退出，点击注册，注册页面就会出现提示信息
    # flash(f'{word} is no longer in your word list.')
    return "success"


@userService.route("/<username>/userpage", methods=['GET', 'POST'])
def userpage(username):
    '''
    用户界面
    :param username: 用户名
    :return: 返回用户界面
    '''
    # 未登录，跳转到未登录界面
    if not session.get('logged_in'):
        return render_template('not_login.html')

    # 用户过期
    user_expiry_date = session.get('expiry_date')
    if datetime.now().strftime('%Y%m%d') > user_expiry_date:
        return render_template('expiry.html', expiry_date=user_expiry_date)

    # 获取session里的用户名
    username = session.get('username')

    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)

    if request.method == 'POST':  # when we submit a form
        content = request.form['content']
        f = WordFreq(content)
        lst = f.get_freq()
        return render_template('userpage_post.html',username=username,lst = lst, yml=Yaml.yml)

    elif request.method == 'GET':  # when we load a html page
        d = load_freq_history(user_freq_record)
        lst = pickle_idea2.dict2lst(d)
        lst2 = []
        for t in lst:
            lst2.append((t[0], len(t[1])))
        lst3 = sort_in_descending_order(lst2)
        words = ''
        for x in lst3:
            words += x[0] + ' '
        visited_articles, today_article, result_of_generate_article = get_today_article(user_freq_record, session.get('visited_articles'))
        session['visited_articles'] = visited_articles
        # 通过 today_article，加载前端的显示页面
        return render_template('userpage_get.html',
                               admin_name=ADMIN_NAME,
                               username=username,
                               session=session,
                               # flashed_messages=get_flashed_messages(), 仅有删除单词的时候使用到flash，而删除单词是异步执行，这里的信息提示是同步执行，所以就没有存在的必要了
                               today_article=today_article,
                               result_of_generate_article=result_of_generate_article,
                               d_len=len(d),
                               lst3=lst3,
                               yml=Yaml.yml,
                               words=words)

@userService.route("/<username>/mark", methods=['GET', 'POST'])
def user_mark_word(username):
    '''
    标记单词
    :param username: 用户名
    :return: 重定位到用户界面
    '''
    username = session[username]
    user_freq_record = path_prefix + 'static/frequency/' + 'frequency_%s.pickle' % (username)
    if request.method == 'POST':
        # 提交标记的单词
        d = load_freq_history(user_freq_record)
        lst_history = pickle_idea2.dict2lst(d)
        lst = []
        for word in request.form.getlist('marked'):
            lst.append((word, [get_time()]))
        d = pickle_idea2.merge_frequency(lst, lst_history)
        if len(lst_history) > 999:
            flash('You have way too many words in your difficult-words book. Delete some first.')
        else:
            pickle_idea2.save_frequency_to_pickle(d, user_freq_record)
            flash('Added %s.' % (', '.join(request.form.getlist('marked'))))
        return redirect(url_for('user_bp.userpage', username=username))
    else:
        return 'Under construction'

def get_time():
    '''
    获取当前时间
    :return: 当前时间
    '''
    return datetime.now().strftime('%Y%m%d%H%M')  # upper to minutes

