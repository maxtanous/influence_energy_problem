from Sentiment import Sentiment
from Graph import Graph

SENTIMENT_CITIES = ['boise', 'twin_falls', 'meridian', 'nampa', 'sun_valley', 'idaho_falls']
class InfluenceEnergyProblem: 

    def __init__(self, to_tokenize):
        self.senitiment_cities = SENTIMENT_CITIES
        self.to_tokenize = to_tokenize

    def get_city_thresholds(self):
        for city in self.senitiment_cities:
            city_sentiment = Sentiment(city, self.to_tokenize)
            city_sentiment.run()

prob = InfluenceEnergyProblem(True)
prob.get_city_thresholds()