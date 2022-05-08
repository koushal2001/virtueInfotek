from Text_Rank import summarize_by_Text_Rank
from LexRank import summarize_by_LexRank

from lsa_summarizer import LsaSummarizer
import nltk
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import tkinter as tk 
from tkinter import filedialog

import sys
import os
import collections
import nltk.data
import string
import math
import features
import traceback
import time
import nltk.corpus
import nltk.stem.porter

import textClasses as tc 
import cluster
import fuzzy
import rules

CUE_PHRASE_FILE = 'bonus_words'
STIGMA_WORDS_FILE = 'stigma_words'

def pre_process_text(text):

    while text[0] == "\n":
        text = text[1:]
        
    text = text.split('\n', 1)
    title = tc.Title(text[0], [])
    text = text[1].replace(u"\u2018", '\'').replace(u"\u2019", '\'').replace(u"\u201c",'"').replace(u"\u201d", '"')
    words = dict()
    sentences = []
    
    sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    detected_sentences = sentence_detector.tokenize(text.strip())
    stopwords_list = nltk.corpus.stopwords.words('english')
    stemmer = nltk.stem.porter.PorterStemmer()
    
    #Pre-process title
    tokens = nltk.word_tokenize(title.original)
    tokens = [token for token in tokens if token not in stopwords_list]
    part_of_speech = nltk.pos_tag(tokens)
    for (token, word_pos) in zip(tokens, part_of_speech):
        token = token.lower()
        if (token not in words) and (token not in list(string.punctuation) and (token not in stopwords_list)):
                words[token] = tc.Word(stemmer.stem(token), word_pos, [(lemma, stemmer.stem(lemma)) for synset in nltk.corpus.wordnet.synsets(token) for lemma in synset.lemma_names()])
        title.bag_of_words.append(token)

    #Pre-process text
    for detected_sentence in detected_sentences:
        
        tokens = nltk.word_tokenize(detected_sentence)
        tokens = [token for token in tokens if token not in stopwords_list]
        if tokens:
            part_of_speech = nltk.pos_tag(tokens)
            bag_of_words = []
            stemmed_bag_of_words = []
            for (token, word_pos) in zip(tokens, part_of_speech):
                token = token.lower()
                if (token not in list(string.punctuation) and (token not in stopwords_list)):
                    if (token not in words):
                        words[token] = tc.Word(stemmer.stem(token), word_pos, [(lemma, stemmer.stem(lemma)) for synset in nltk.corpus.wordnet.synsets(token) for lemma in synset.lemma_names()])
                    elif token in words:
                        words[token].increment_abs_frequency()
                    bag_of_words.append(token)
                    stemmed_bag_of_words.append(stemmer.stem(token))
            if (len(bag_of_words) != 0 or len(stemmed_bag_of_words) != 0):
                sentences.append(tc.Sentence(detected_sentence, len(sentences) + 1, [], [], None))
                sentences[-1].bag_of_words = list(bag_of_words)
                sentences[-1].stemmed_bag_of_words = list(stemmed_bag_of_words)        
    return [title, sentences, words]

def process_input():
    root = tk.Tk()
    root.withdraw()
    text_file = filedialog.askopenfilename()

    with open(text_file, 'r') as f:
        text = f.read()
    f.closed

    summarized_LexRank_Text = summarize_by_LexRank.summarize(text)  
    summarized_TextRank_Text = summarize_by_Text_Rank.summarize(summarized_LexRank_Text)  
    summarizer = LsaSummarizer()

    stopword = stopwords.words('english')
    summarizer.stop_words = stopword
    summary =summarizer(summarized_TextRank_Text, 3)
    summarized_output = summary
    return {"text": text, "summarized":summary}

def resource_loader():
    resources = dict()
    path = os.path.dirname(os.path.realpath(__file__)) + '/extra_files/'
    resource_files = [file.split()[0] for file in os.listdir(path)]
    for resource_file_name in resource_files:
        with open(path + "/"+resource_file_name, 'r') as f:
            text = f.read()
        f.closed
        resources[resource_file_name.split('.')[0]] = set(list(text.split('\n')))
    return resources

def filter_using_clusters(sentences, percentage, clusters):
    number_sentences = math.floor(percentage * len(sentences))
    sentences = sorted(sentences, key=lambda x: x.rank, reverse=True)
    clusters_counter = [0] * len(clusters)
    sentence_counter = 0;
    chosen_sentences = []
    while len(chosen_sentences) < number_sentences:
        sentence_counter = 0
        for i in range(0, len(clusters)):
            for j in range(0, len(sentences)):
                if (clusters_counter[i] == min(clusters_counter) and clusters[i].count(sentences[j].position) == 1):
                    chosen_sentences.append(sentences[j])
                    clusters[i].remove(sentences[j].position)
                    if (len(clusters[i]) == 0):
                        clusters_counter[i] = sys.maxsize
                    else:
                        clusters_counter[i] += 1
                    break;
            if (len(chosen_sentences) >= number_sentences):
                break;
    chosen_sentences = sorted(chosen_sentences, key=lambda x: x.position)
    return chosen_sentences

def main():
        processed_input = process_input()
        text = processed_input['text']
        percentage = 25
        threads = 50
        resources = resource_loader()
        preprocessed_text = pre_process_text(text)
        preprocessed_text[1] = sorted(preprocessed_text[1], key=lambda x: x.position)
        keyword_feature_value = features.keyword_feature(preprocessed_text[1], preprocessed_text[2])
        title_word_feature_value = features.title_word_feature(preprocessed_text[0], preprocessed_text[1])
        sentence_location_feature_value = features.sentence_location_feature(preprocessed_text[1])
        sentence_length_feature_value = features.sentence_length_feature(preprocessed_text[1])
        proper_noun_feature_value = features.pos_tag_feature(preprocessed_text[1], preprocessed_text[2], 'NNP')
        cue_phrase_feature_value = features.phrase_feature(preprocessed_text[1], resources[CUE_PHRASE_FILE])
        stigma_phrase_feature_value = features.phrase_feature(preprocessed_text[1], resources[STIGMA_WORDS_FILE])
        numerical_data_feature_value = features.pos_tag_feature(preprocessed_text[1], preprocessed_text[2], 'CD')
        k_means_result = cluster.k_means(preprocessed_text[1], preprocessed_text[2], percentage, threads)

        sentences_feature_list = []
        for (
    keyword_value,
    title_word_value,
    sentence_location_value,
    sentence_lenght_value,
    proper_noun_value,
    cue_phase_value,
    stigma_word_value,
    numerical_data_value,
    ) in zip(
    keyword_feature_value,
    title_word_feature_value,
    sentence_location_feature_value,
    sentence_length_feature_value,
    proper_noun_feature_value,
    cue_phrase_feature_value,
    stigma_phrase_feature_value,
    numerical_data_feature_value,
    ):
            sentences_feature_list.append({
            'keyword': keyword_value,
            'title_word': title_word_value,
            'sentence_location': sentence_location_value,
            'sentence_length': sentence_lenght_value,
            'proper_noun': proper_noun_value,
            'cue_phrase': cue_phase_value,
            'nonessential': stigma_word_value,
            'numerical_data': numerical_data_value,
            })

        fuzzy.set_fuzzy_ranks(preprocessed_text[1], sentences_feature_list)
        chosen_sentences = filter_using_clusters(preprocessed_text[1], float(percentage)/100, k_means_result[1])
        all_sentences_information = []
        for sentence in preprocessed_text[1]:
            chosen = 0
            if (sentence in chosen_sentences):
                chosen = 1
            all_sentences_information.append([sentence.position, sentence.rank, chosen])
        summarized_output = ""
        for sentence in chosen_sentences:
                summarized_output = summarized_output + sentence.original + ' '
        return(summarized_output)

##summarized_output = main()
##print(summarized_output)




