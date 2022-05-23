import re
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def removeSpecialChars(s):
    return re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', s).split()


def calculateBOW(wordset,l_doc):
    tf_diz = dict.fromkeys(wordset,0)
    for word in l_doc:
      tf_diz[word]=l_doc.count(word)
    return tf_diz


def bagofwords(obj):
    if len(obj.titleBox) < 1:
        print("No Title Exists to Execute Bag of Words. Returning -1")
        return -1
    wordset = np.array(removeSpecialChars(obj.titleBox[0]))

    for i in range(1, len(obj.titleBox)):
        w1 = np.array(removeSpecialChars(obj.titleBox[i]))
        wordset = np.append(wordset, w1)

    print("Words from Union of All Titles: ", wordset)
    print()

    ##### Bag of Words #######

    df_bow = []
    for i in range(len(obj.titleBox)):
        d = calculateBOW(wordset, removeSpecialChars(obj.titleBox[i]))
        df_bow.append(d)

    df_bow = pd.DataFrame(df_bow)
    print(df_bow.head(20))
