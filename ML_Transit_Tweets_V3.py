#location word count
#

import os
import csv
import nltk
import re
import numpy as np
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
from nltk import ngrams
from nltk.tokenize import word_tokenize
from functools import reduce
from collections import Counter
import operator

#function to remove URLs
def remove_urls (vTEXT):
    vTEXT =re.sub(r'http\S+', '', vTEXT)
    return(vTEXT)

corpus=[]
temparray=[]
tok_corp2=[]
loading=0

file = open(r"Input.txt",'r')
lines=file.readlines()
file.close()
for line in lines:
    print("Preprocessing:",loading)
    loading=loading+1
    #line=remove_urls(line) #remove URLs
    #line=' '.join(word for word in line.split(' ') if not word.startswith('@')) #remove mentions
    #line=line.lower() #make lowercase
    #line=re.sub(r'[^\w]', ' ', line) #remove symbols
    corpus.append(line) #put the processed tweets in corpus 

tok_corp=[nltk.word_tokenize(sent) for sent in corpus]

#Vwords=['bus','train','trains','station','skytrain','driver','buses','sad','night','sleep','wish','miss','tomorrow','lol','bad','feel','love','sick','bed','feeling','fun','bored','little','phone','life','house','ready','missing','stupid','game','gas','petrol','radio','tv','gym','hard','motivated','motivation','sandwich','inch','happy','tour','tours']
#Vbigrams=['at stop','bus stop','the stop','stop at','canada line','expo line','millennium line','bus driver','minutes late','on the','going to','at the','waiting at','there is','my bus','back to','i want','i know','i had','to see','think i','i hope','woke up','miss you','go train','train wreck','school bus','police station','under the','i will','so much','too much','i should','at work','of my','of thought']
Vwords=['bus','train','trains','station','ctrain','driver','buses','sad','night','sleep','wish','miss','tomorrow','lol','bad','feel','love','sick','bed','feeling','fun','bored','little','phone','life','house','ready','missing','stupid','game','gas','petrol','radio','tv','gym','hard','motivated','motivation','sandwich','inch','happy','tour','tours']
Vbigrams=['at stop','bus stop','the stop','stop at','blue line','red line','red line','bus driver','minutes late','on the','going to','at the','waiting at','there is','my bus','back to','i want','i know','i had','to see','think i','i hope','woke up','miss you','go train','train wreck','school bus','police station','under the','i will','so much','too much','i should','at work','of my','of thought']
#replace ctrain with streetcar, blue line with Line 1 red line with line 2 and red line with line 3

bigrams=[]
tempbigrams=[]
for tweet in corpus:
    _bigrams=ngrams(tweet.split(),2)
    __bigrams=list(_bigrams)
    for bigram in __bigrams:
        bigram_=bigram[0]+" "+bigram[1]
        tempbigrams.append(bigram_)
    bigrams.append(tempbigrams)
    tempbigrams=[]

print(bigrams)

def bagofwords(sentence, words): #function to create bag of words
    sentence_words = sentence
    # frequency word count
    bag = np.zeros(len(words))
    for sw in sentence_words:
        for i,word in enumerate(words):
            if word == sw: 
                bag[i] += 1                
    return np.array(bag)

newcorpus=[]
newcorpusbigrams=[]

for i in np.arange(len(tok_corp)):
    templist=list(bagofwords(tok_corp[i],Vwords))
    templist=list(templist)
    newcorpus.append(templist)

for i in np.arange(len(bigrams)):
    templist=list(bagofwords(bigrams[i],Vbigrams))
    templist=list(templist)
    newcorpusbigrams.append(templist)

for i in np.arange(len(bigrams)):
    newcorpus[i].extend(newcorpusbigrams[i])

exportcorpus=newcorpus # i don't know why i did this

f= open("Corpus.txt","w") #this step outputs a txt file only so that we can easily remove the [ and ] from the list and output just numbers into a txt file
for i in np.arange(len(tok_corp)): #this file will be deleted later, will be replaced by outputtransit.txt
     f.write(str(exportcorpus[i]))
     f.write("\n")
f.close()

with open("Corpus.txt",encoding="utf-8") as infile, open("Output.txt", 'w',encoding="utf-8") as outfile:
    for line in infile:
        line2=line.replace("[", "") #remove [ from start of list 
        line3=line2.replace("]", "") #remove ] from end of list
        outfile.write(line3)  
outfile.close()
infile.close()

os.remove("Corpus.txt") #deleted, we don't need it