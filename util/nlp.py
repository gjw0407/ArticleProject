# from util.read_excel_file import read_csv
# from util.get_articles import *
# from timeloop import Timeloop
# from datetime import timedelta
# from util.StoreArticle import saveArticle
# import time

# timeloop = Timeloop()
import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

okt = Okt()

# @timeloop.job(interval=timedelta(seconds=600))
# def sample_job_every_2s():
#     url = [read_csv()]
#     news = NewsStand()
#     news.checkChanges(url)
#     saveArticle(news)

#     # Clustering
#     #bagofwords(news)


# timeloop.start()
# while True:
#     time.sleep(300)
import sqlite3
path = "C:/Users/Administrator/Desktop/workspace/vscode/articleProject/BE/articleTopic/db.sqlite3"

# 특수문자 모두 제거 안함 -> '코로나-19'등 정보로 활용할 수 있는 가능성 -> 수정 : 특수문자 제거
import re
country_div_symbols = ["·", "-"]
country_abbrev_dict = {"한" : "대한민국",
                       "미" : "미국",
                       "러" : "러시아",
                       "중" : "중국",
                       "일" : "일본"
                      }
'''
타이완(臺灣): 臺(대)
독일(獨逸): 獨(독)
미국(美國): 美(미)[2]
영국(英國): 英(영)
오스트레일리아(濠洲, 호주): 濠(호)
인도(印度): 印(인)
일본(日本): 日(일)
조선민주주의인민공화국: 北(북), 朝(조)[3]
중국(中國): 中(중)
베트남: 월남(중국어: 越南, 병음: Yuènán)의 첫 글자를 딴 越(월)
태국(泰國): 泰(태)
'''
country_chinese_char_dict = {
                       "臺" : "대만",
                       "獨" : "독일",
                       "北" : "북한",
                       "日" : "일본",
                       "中" : "중국",
                       "美" : "미국",
                       "英" : "영국",
                       "韓" : "한국"
                      }

def _replace_country_by_dots(sentence):
  # sentence = re.sub('[\"\']',' ', sentence)
  # sentence = re.sub('[-=+,·#/\?:^$.@*※~&%ㆍ!』\\‘|\(\)\[\]\<\>`…》]','', sentence)
  # 밑에 주석 다시 쓰려면 함수 수정 필요(문자 바꾸고 문장 길이 체크하는 로직)
  symbol_index = []
  i = 0
  while i < len(sentence):
    if i==0 or i==len(sentence)-1:
      i+=1
      continue
    # if sentence[i] 가 영어나 한글일 경우
    #  continue
    if sentence[i] in country_div_symbols and sentence[i-1] in country_abbrev_dict and sentence[i+1] in country_abbrev_dict:
      # 한·러   "미-중"
      country_first = country_abbrev_dict[sentence[i-1]]
      country_last = country_abbrev_dict[sentence[i+1]]
      sentence = sentence[:i-1] + country_first + " " + country_last + sentence[i+2:]
      i+=len(country_first) + len(country_last)
    else:
      i+=1
  return sentence

def _replace_country_by_no_space(sentence):
  # 특수문자 없는 경우
  # 한미
  country_idx = []
  idx = 1 
  while(idx < len(sentence)):
    # if sentence[i] 가 영어나 한글일 경우 : 경미한
    #  continue
    if sentence[idx-1] in country_abbrev_dict and sentence[idx] in country_abbrev_dict:
      country_first = country_abbrev_dict[sentence[idx-1]]
      country_last = country_abbrev_dict[sentence[idx]]
      sentence = sentence[:idx-1] + country_first+ " " + country_last + sentence[idx+1:]
      idx+=len(country_first) + len(country_last)
    else:
      idx+=1
  return sentence

def _replace_country_by_char(sentence):
  for chinese_char, country_name in country_chinese_char_dict.items():
    sentence = sentence.replace(chinese_char, country_name+" ")
  return sentence

def replace_country(sentence:str):
  sentence = _replace_country_by_dots(sentence)
  # sentence = _replace_country_by_no_space(sentence)
  sentence = _replace_country_by_char(sentence)
  return sentence

def replace_politics(sentence):
  politics_chinese_char_dict = {
                       "與" : "여당",
                       "尹" : "윤석열",
                       "野" : "야당"
                      }
  for chinese_char, politics_name in politics_chinese_char_dict.items():
    sentence = sentence.replace(chinese_char, politics_name+" ")
  return sentence  

def morph(sentence):
  # print(sentence)
  sentence = replace_country(sentence)
  sentence = replace_politics(sentence)
  # print(sentence)
  return okt.nouns(sentence)

label = 1

def nlp():
  con = sqlite3.connect(path) # 해보고
  cur = con.cursor()
  # for table in cur.execute('SELECT name FROM sqlite_master WHERE type = "table"'):
  #   print(table)
  cur = con.cursor().execute('SELECT * FROM articleHeatMap_article') # where date = sysdate -1
  cols = [column[0] for column in cur.description]
  articles = pd.DataFrame.from_records(data=cur.fetchall(), columns=cols)
  articles["title_noun"] = articles["title"].apply(lambda x : morph(x))

  vectorizer = CountVectorizer() # HashingVectorizer(n_features=10000, stop_words=None)
  title_noun_list = list(map(" ".join, articles['title_noun'].tolist()))
  vectorizer.fit(title_noun_list)
  title_noun_vector= vectorizer.transform(title_noun_list).toarray()
  # articles["title_noun_vector"]= pd.Series(title_noun_vector)

  similarity = [[0]*title_noun_vector.shape[0] for _ in range(title_noun_vector.shape[0])]


  for i in range(title_noun_vector.shape[0]):
    for j in range(title_noun_vector.shape[0]):
      cos_sim = cosine_similarity(title_noun_vector[i:i+1],title_noun_vector[j:j+1])
      similarity[i][j] = float(cos_sim[0])
      similarity[j][i] = float(cos_sim[0])
  # similarity

  # 컬럼으로 넣기
  i = [-1]
  def bow():
    i[0]+=1
    return title_noun_vector[i[0]]

  articles["title_bow"] = articles.id.apply(lambda x:bow())

  bow_sum = np.array([0]*title_noun_vector.shape[1])

  for t in title_noun_vector:
    bow_sum += t
  bow_sum = list(bow_sum)

  for i in range(len(bow_sum)):
    bow_sum[i] = [i,bow_sum[i]]
  bow_sum.sort(key=lambda x:-x[1])

  dic = {}

  for k,v in vectorizer.vocabulary_.items():
    dic[v] = k



  labels = [False] * title_noun_vector.shape[0]
  label_info = []
  def labeling(bow_idx, cnt):
    global label
    change_queue = []
    for i in range(title_noun_vector.shape[0]):
      if not labels[i] and title_noun_vector[i][bow_idx] > 0:
        change_queue.append(i)
    if len(change_queue) < cnt:
      return
    for q in change_queue:
      labels[q] = label
    label_info.append([dic[bow_idx], label])
    label+=1
    
  for vocab, cnt in bow_sum:
    labeling(vocab, 3) # 이값은 설정 해야함

  from collections import defaultdict
  class News_clustering:
    def __init__(self, similarity, eps=0.25, min_samples=2, labels = None):
      if labels is None:
        self.labels = [0] * similarity.shape[0]
      else:
        self.labels = labels
      self.max_label = max(self.labels)
      self.eps = eps
      self.similarity = np.array(similarity)
      self.min_samples = min_samples
      labels_dict = defaultdict(list)
      for i in range(1, self.max_label+1):
        for j in range(self.similarity.shape[0]):
          if self.labels[j] == i:
            labels_dict[i].append(j)
      self.labels_dict = labels_dict
    
    def cluster_curr_idx(self,idx):
      labels_dict = self.labels_dict
      max_similarity = 0
      max_similarity_label = -1

      for label in labels_dict:
        curr_similarity = []
        for i in labels_dict[label]:
          if self.similarity[i][idx] > self.eps:
            curr_similarity.append(self.similarity[i][idx])
        if len(curr_similarity) > self.min_samples:
          curr_similarity.sort(reverse=True)
          curr_similarity_avg = sum(curr_similarity[:self.min_samples]) / self.min_samples
          if curr_similarity_avg > max_similarity:
            max_similarity_label = label
      if max_similarity_label !=-1:
        self.labels[idx] = max_similarity_label

    def cluster(self): # min_samples = 1 로 고정 -> 2개로 수정
      for i in range(self.similarity.shape[0]):
        if self.labels[i]>0:
          continue
        self.cluster_curr_idx(i)

      return self.labels

  cls = News_clustering(similarity, 0.1, 1, labels) # similarity, 개수
  new_labels = cls.cluster()
  articles['label'] = new_labels
  # print(articles['label'].head())
  # print(articles[['title_noun','label']].head())
  
  def label_to_string(x):
    return label_info[x+1][0]
  articles["label_to_string"] = articles['label'].apply(lambda x:label_info[x-1][0])
  # print(articles[['title_noun','label','label_to_string']])

  from collections import Counter
#   {
#                 "x":'윤석열',"y": 빈도수
#               }
  output = [{"x" : label[0], "y": 0} for i, label in enumerate(label_info)]
  for l in new_labels:
    if not l: # False 처리
      continue
    output[l-1]["y"]+=1
  return output