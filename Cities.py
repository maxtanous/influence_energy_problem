import googlemaps
from geopy.distance import geodesic
import io
import pandas as pd

NUMBER_OF_NEIGHBORS = 3

class Cities: 

    def __init__(self):

        self.city_cords_dictionary = {}
        self.city_distances_dictionary = {}
        self.cities = []
        self.city_neighbors = []
        self.read_in_cities()
        self.calculate_distances()
        self.calculate_closest_cities()

    def read_in_cities(self):
        excel_data_df = pd.read_excel( 'Idaho Cities.xlsx', sheet_name='Sheet1',  header=None)
        city_coordinates = excel_data_df.to_dict()
        for city in city_coordinates:
            self.cities.append(city_coordinates[city][0])
        self.city_cords_dictionary = city_coordinates

    def calculate_distances(self):
        results_dict = {}
        temporary_city = {}

        cities = self.city_cords_dictionary
        for city in cities:

                city_data = cities[city]
                name = city_data[0]
                
                city_long = city_data[1]
                city_lat = city_data[2]
                city_cords = (city_long, city_lat)
                for other_city in cities:
                    other_city_data = cities[other_city]
                    other_city_name = other_city_data[0]
                    other_city_long = other_city_data[1]
                    other_city_lat = other_city_data[2]
                    other_city_cords = (other_city_long, other_city_lat)
                    city_distance = geodesic(city_cords, other_city_cords).miles
                    temporary_city.update({other_city_name: city_distance})
                    if (other_city) > int(8):
                        results_dict.update({name : temporary_city})
                        temporary_city = {}

        self.city_distances_dictionary = results_dict

    def calculate_closest_cities(self):
        city_dictionary = self.city_distances_dictionary
        distance_dictionary = {}
        cities = self.cities
        for city in cities:
            city_closest_neighbors = {}
            vals_array = []
            town_dictionary = city_dictionary[city].items()
            for key, value in town_dictionary:
                vals_array.append(value)
            sorted_list = (sorted(vals_array))[1:NUMBER_OF_NEIGHBORS +2]
            city_array = []
            for distance in sorted_list:
               city_name = next(key for key, value in town_dictionary if value == distance)
               city_array.append(city_name)
            city_closest_neighbors.update({city : city_array})
            self.city_neighbors.append(city_closest_neighbors)
        
            
        
            




        



            
               



                





