from queue import PriorityQueue
from multiprocessing.pool import ThreadPool
import json
import argparse
# import pkuseg
from nltk import word_tokenize
# 基于关键词json字典的简单问答
tfidf = json.load(open('./data/chat.json',encoding='UTF-8'))
# bm25 = json.load(open('rawdata/chat.json',encoding='UTF-8'))
text = ''
q = PriorityQueue()
# method = 'TFIDF'

def seg(article):
    words = word_tokenize(article)
    # print(words)
    return words

def score(num):
    global text, q
    tmp = tfidf[num]['question']
    tmp_score = 0
    for token in text:
        if token in tmp.keys():
            tmp_score += tmp[token]
    q.put((-tmp_score, num))

def chat(inputs):
    global text, q
    text = seg(inputs)
    q = PriorityQueue()
    pool = ThreadPool(4)
    pool.map(score, list(tfidf.keys()))
    pool.close()
    num = q.get()[1]
    answer = tfidf[num]['answer']
  # answer = ' '.join(seg(tfidf[num]['answer']))
    print(f'Answer--> {answer}')
    return answer

if __name__ == '__main__':
  # parser = argparse.ArgumentParser(description='manual to this script')
  # parser.add_argument('--method', type=str, default = 'BM25')
  # args = parser.parse_args()
  # method = args.method
  # print(f"本次对话使用的是 {method}")
  while True:
    QA()