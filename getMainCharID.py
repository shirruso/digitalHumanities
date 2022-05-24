import json
import requests
from getMoviesPerCountry import countries


def open_all_json_files():
    for country in countries:
        path = './json files/%s.json' % country.name
        with open(path, 'r') as json_file:
            movies_per_country = json.load(json_file)
            json_dict = {}
            for years_range, movies_arr in movies_per_country.items():
                updated_movies_arr = expand_movie_dict(movies_arr)
                json_dict.update({years_range: updated_movies_arr})
        with open(path, 'w') as outfile:
            json.dump(json_dict, outfile, indent=4)
