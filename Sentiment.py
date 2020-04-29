import nltk.data
import os
# first, we import the relevant modules from the NLTK library
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize

class Sentiment:

    def __init__(self, city_name, to_tokenize):
        self.sid = SentimentIntensityAnalyzer()
        self.city_name = city_name
        self.to_tokenize = to_tokenize
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.filenames = self.get_article_names(city_name)

    def get_article_names(self, city_name):
        filenames = []
        for file in os.listdir('articles/'+ city_name ):
            filename = os.fsdecode(file)
            filenames.append(filename)
        return filenames

    def get_sentiment_no_tokenize(self):
        article_sentiments = {}
        for filename in self.filenames:
            with open('articles/' + self.city_name +'/' + filename, 'r') as file:
                data = file.read().replace('\n', '')
                scores = self.sid.polarity_scores(data)
                article_sentiments[filename] = scores['compound']
        return article_sentiments

    def get_sentiment_tokenize(self):
        article_sentiments = {}
        for filename in self.filenames:
            with open('articles/' + self.city_name +'/' + filename, 'r') as file:
                data = file.read().replace('\n', '')
                sentences = self.tokenizer.tokenize(data)
                num_sentences = len(sentences)
                compound_score = 0
                for sentence in sentences:
                    scores = self.sid.polarity_scores(sentence)
                    compound_score += scores['compound']
                article_sentiments[filename] = compound_score/num_sentences
        return article_sentiments

                       

    def run(self):
        sentiment = {}
        overall_score = 0
        if self.to_tokenize:
            sentiment = self.get_sentiment_tokenize()
        else:
            sentiment = self.get_sentiment_no_tokenize()
        for key in sentiment:
            overall_score += sentiment[key]
        overall_score = overall_score / len(self.filenames)
        print("City Name: ", self.city_name)
        print("Sentiment Scores For Each Article: ", sentiment)
        print("Overall Compound Score: ", overall_score)
        print('------------------------------------')


