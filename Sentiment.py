import nltk.data
import os
# first, we import the relevant modules from the NLTK library
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize
from striprtf.striprtf import rtf_to_text
from nltk.corpus import stopwords

class Sentiment:

    def __init__(self, city_name, to_tokenize, directory):
        self.sid = SentimentIntensityAnalyzer()
        self.city_name = city_name
        self.to_tokenize = to_tokenize
        self.directory = directory
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.filenames = self.get_article_names(city_name)

    def get_article_names(self, city_name):
        filenames = []
        for file in os.listdir(self.directory + '/'+ city_name ):
            filename = os.fsdecode(file)
            filenames.append(filename)
        return filenames

    def get_sentiment_no_tokenize(self):
        article_sentiments = {}
        for filename in self.filenames:
            with open('articles/' + self.city_name +'/' + filename, 'r') as file:
                data = file.read().replace('\n', '')
                rtf = file.read().replace('\n', '')
                data = rtf_to_text(rtf)
                words = self.tokenizer.word_tokenize(data)

    def clean_data(self, data):
        stop_words = set(stopwords.words('english')) 
        words = nltk.word_tokenize(data)
        words = [word for word in words if len(word) > 1]
        words = [word for word in words if not word.isnumeric()]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in stop_words]
        return words
    
    def get_sentiment_tokenize(self):
        article_sentiments = {}
        trip = False
        for filename in self.filenames:
            if trip:
                return article_sentiments
            with open(self.directory + '/' + self.city_name +'/' + filename, 'r') as file:
                rtf = file.read().replace('\n', '')
                data = rtf_to_text(rtf)
                sentences = self.tokenizer.tokenize(data)
                num_sentences = len(sentences)
                compound_score = 0
                for sentence in sentences:
                    scores = self.sid.polarity_scores(sentence)
                    compound_score += scores['compound']
                article_sentiments[filename] = compound_score/num_sentences
            
        return article_sentiments


    def get_word_frequency(self, word):
        city_freq_dict = {}
        word_count = 0
        trip = False
        for filename in self.filenames:
            if trip:
                return city_freq_dict
            with open(self.directory + '/' + self.city_name +'/' + filename, 'r') as file:
                rtf = file.read().replace('\n', '')
                data = rtf_to_text(rtf)
                words = self.clean_data(data)
                count = words.count(word)
                word_count += count
            #city_freq_dict[filename] = count
      
        #print(city_freq_dict)
        print(self.city_name + ": ", word_count/len(self.filenames))
    
                
                


                       

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
        #print("Sentiment Scores For Each Article: ", sentiment)
        print("Overall Compound Score: ", overall_score)
        print('------------------------------------')


# sen = Sentiment('boise', True, 'articles')
# sen.get_word_frequency()