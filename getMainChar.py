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


def expand_movie_dict(movies_arr):
    updated_movies_arr = []
    for movie in movies_arr:
        addition = get_main_character(movie['id'])
        if len(addition) > 0:
            movie.update(addition)
            updated_movies_arr.append(movie)
    return updated_movies_arr

# Given movie_id we will use TMDB API to get the main character name as well as his gender.


def get_main_character(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/%s/credits?api_key=dafbfad599cde5d98a5d1c68cef38b1c' % movie_id)
    if not response.ok:
        return {}
    response_json = response.json()
    # the main character is located first in 'cast' array
    if len(response_json['cast']) == 0:
        return {}
    main_character = response_json['cast'][0]
    name = main_character['name']
    # 1 - Female, 2 - Male
    gender = main_character['gender']
    return {'name': name, 'gender': gender}