from __future__ import print_function
import pymysql
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import time;


def get_text():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='kb-policy')
    mycursor = conn.cursor()
    sql = 'select policy_content from kb_policy_collect limit 500'
    mycursor.execute(sql)
    contentlist = []
    alldata = mycursor.fetchall()
    text = ''
    for content in alldata:
        contentlist.append(content[0])
        text += content[0]
    print('列表总长度: ', len(contentlist))
    mycursor.close()
    conn.close()
    return text

def text_rank(text):
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    return tr4w.get_keywords(40, word_min_len=2)

def save_rank(words):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='kb-policy')
    mycursor = conn.cursor()
    localtime = time.localtime(time.time())
    for id, item in enumerate(words):
        sql = 'insert into policy_key_weight values(%s,%s,%s,%s)'
        mycursor.execute(sql, (id, item.word, item.weight, localtime))
    conn.commit()
    mycursor.close()
    conn.close()

save_rank(text_rank(get_text()))


