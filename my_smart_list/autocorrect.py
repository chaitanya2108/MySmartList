import pandas as pd
import numpy as np
import textdistance
import re
from collections import Counter

words = []
with open('data.txt', 'r') as f:
    file_name_data = f.read()
    file_name_data=file_name_data.lower()
    words = re.findall('\w+',file_name_data)
# This is our vocabulary
V = set(words)

word_freq = {}  
word_freq = Counter(words)


probs = {}     
Total = sum(word_freq.values())    
for k in word_freq.keys():
    probs[k] = word_freq[k]/Total

def my_autocorrect(input_word):
    input_word = input_word.lower()
    if input_word in V:
        return input_word
    else:
        sim = [1-(textdistance.Jaccard(qval=2).distance(v,input_word)) for v in word_freq.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df = df.rename(columns={'index':'Word', 0:'Prob'})
        df['Similarity'] = sim
        output = df.sort_values(['Similarity'], ascending=False).head(3)
        return(output.Word.iloc[0])

def autocorrect(list1):
    #list1 = ['gua', 'cerel']
    for i in range(len(list1)):
        print(my_autocorrect(list1[i]))
        re = str(my_autocorrect(list1[i]))
        list1[i] = re
    print(list1)
    return list1

