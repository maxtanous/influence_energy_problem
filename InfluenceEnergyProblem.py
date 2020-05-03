from Sentiment import Sentiment
from Graph import Graph
SENTIMENT_CITIES = ['boise', 'twin_falls', 'meridian', 'nampa', 'sun_valley', 'idaho_falls', 'rexburg', 'coeur_dalene', 'hailey', 'lewiston']

### FOR LEGISLSATION 
#SENTIMENT_CITIES = ['boise', 'twin_falls', 'meridian', 'sun_valley', 'idaho_falls', 'coeur_dalene', 'lewiston']
class InfluenceEnergyProblem: 

    def __init__(self, to_tokenize, doc_type):
        self.senitiment_cities = SENTIMENT_CITIES
        self.to_tokenize = to_tokenize
        self.document_type = doc_type

    def get_city_thresholds(self):
        for city in self.senitiment_cities:
            city_sentiment = Sentiment(city, self.to_tokenize, self.document_type)
            city_sentiment.run()

    def get_word_frequency(self):
        for city in self.senitiment_cities:
            city_sentiment = Sentiment(city, self.to_tokenize, self.document_type)
            city_sentiment.get_word_frequency('biomass')

prob = InfluenceEnergyProblem(True, 'articles')
prob.get_city_thresholds()