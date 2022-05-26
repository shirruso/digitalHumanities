import requests
import json

keys = {'k_64p78757', 'k_ao1xicrn', 'k_cc9uodvl'}

class Country:
    def __init__(self, name, shortcut, language):
        self.name = name
        self.shortcut = shortcut
        self.language = language


countries = [
             # Country('Afghanistan', 'af', 'ps')
             # Country('Egypt', 'eg', 'ar')
             # Country('Lebanon', 'lb', 'ar'),
             # Country('Turkey', 'tr', 'tr')
             # Country('Iran', 'ir', 'ar'),
            Country('France', 'fr', 'fr')
             # Country('Germany', 'de', 'nl'),
             # Country('Italy', 'it', 'it'),
             # Country('United Kingdom', 'gb', 'en'),
             # Country('Greece', 'gr', 'el'),
             # Country('Poland', 'pl', 'pl'),
             # Country('Russia', 'ru', 'ru'),
             # Country('Japan', 'ja', 'ja'),
             # Country('India', 'in', 'hi'),
             # Country('China', 'cn', 'zh'),
             # Country('United_States', 'us', 'en'),
             # Country('Mexico', 'mx', 'es'),
             # Country('Canada', 'ca', 'en'),
             # Country('Brazil', 'br', 'pt'),
             # Country('Argentina', 'ar', 'es'),
             # Country('Australia', 'au', 'en'),
             # Country('South_Africa', 'za', 'af'),
             # Country('Ethiopia', 'et', 'am'),
             # Country('Nigeria', 'ng', 'en')
             ]

years = ['1960_1979', '1980_1999', '2000_2009', '2010_2012', '2013_2015', '2016_2018', '2019_2022']


def get_movies():
    for country in countries:
        get_movies_per_country(country)


# The function creates a json file which contains all the movies of a particular country according to the years in
# 'years' array


def get_movies_per_country(country):
    json_dict = {}
    for years_range in years:
        json_dict.update({years_range: get_movies_per_years(country, years_range)})
    path = './json files/%s.json' % country.name
    with open(path, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)


def get_movies_by_pages(country, years_range):
    movies = []
    num_of_pages = 3
    release_data_from, release_data_to = years_range[0:4], years_range[5:]
    for i in range(0, num_of_pages):
        response = requests.get(
            'https://imdb-api.com/API/AdvancedSearch/k_64p78757?release_date=%s-01-01,'
            '%s-12-31&countries=%s&languages=%s&count=250&start=%d' % (
                release_data_from, release_data_to, country.shortcut,
                country.language, i * 250 + 1))
        response_json = response.json()
        movies_per_page = response_json['results']
        movies.append(movies_per_page)
    flat_movies = [movie for sublist in movies for movie in sublist]
    return flat_movies


# The function returns an array of movies that have been released over the years. The array contains for each movie
# its id as well as its title.


def get_movies_per_years(country, years_range):
    movies = get_movies_by_pages(country, years_range)
    filtered_movies = []
    for movie in movies:
        response = requests.get('https://api.themoviedb.org/3/movie/%s/credits?api_key=dafbfad599cde5d98a5d1c68cef38b1c'
                                % movie['id'])
        response_json = response.json()
        if (not response.ok) or len(response_json['cast']) == 0:
            continue
        main_character = response_json['cast'][0]
        data = {'id': movie['id'],
                'title': movie['title'],
                'main_character_name': main_character['name'],
                'main_character_gender': main_character['gender'],
                'main_character_role': main_character['character']}
        filtered_movies.append(data)
    return filtered_movies
