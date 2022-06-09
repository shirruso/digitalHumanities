import requests
import json
import imdb

keys = {'k_64p78757', 'k_ao1xicrn', 'k_cc9uodvl', 'k_sej8mhp2', 'k_ay2kvfye'}


class Country:
    def __init__(self, name, shortcut, language, wikidata_key):
        self.name = name
        self.shortcut = shortcut
        self.language = language
        self.wikidata_key = wikidata_key


countries = [
    # Country('Afghanistan', 'af', 'ps'ת ,'Q889')
     Country('Egypt', 'eg', 'ar', 'Q79')
    # Country('Lebanon', 'lb', 'ar', 'Q822'),
    # Country('Turkey', 'tr', 'tr', 'Q43')
    # Country('Iran', 'ir', 'ar', 'Q794'),
    # Country('France', 'fr', 'fr', 'Q142')
    # Country('Germany', 'de', 'nl', 'Q183'),
    # Country('Italy', 'it', 'it', 'Q38'),
    # Country('United Kingdom', 'gb', 'en', 'Q145'),
    # Country('Greece', 'gr', 'el', 'Q41'),
    # Country('Poland', 'pl', 'pl', 'Q36'),
    # Country('Russia', 'ru', 'ru','Q159'),
    # Country('Japan', 'ja', 'ja', 'Q17'),
    # Country('India', 'in', 'hi', 'Q668'),
    # Country('China', 'cn', 'zh', 'Q148),
    # Country('United_States', 'us', 'en', 'Q30'),
    # Country('Mexico', 'mx', 'es', 'Q96'),
    # Country('Canada', 'ca', 'en', 'Q16'),
    # Country('Brazil', 'br', 'pt', 'Q155'),
    # Country('Argentina', 'ar', 'es', 'Q414'),
    # Country('Australia', 'au', 'en', 'Q408'),
    # Country('South_Africa', 'za', 'af', 'Q258'),
    # Country('Ethiopia', 'et', 'am', 'Q115'),
    # Country('Nigeria', 'ng', 'en', 'Q1033')
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
            'https://imdb-api.com/API/AdvancedSearch/k_sej8mhp2?release_date=%s-01-01,'
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
        main_character_name, role_from_imdb = get_role_imdb(movie['id'])
        if main_character_name is None:
            continue
        main_character_gender, role_from_tmdb = get_gender_and_role_tmdb(response_json['cast'], main_character_name)
        if main_character_gender is None:
            continue

        data = {'id': movie['id'],
                'title': movie['title'],
                'release_year': movie['description'][1:-1],
                'plot': movie['plot'],
                'main_character_name': main_character_name,
                'main_character_gender': main_character_gender,
                'main_character_role': [role_from_tmdb, role_from_imdb]}
        filtered_movies.append(data)
    return filtered_movies


# The function receives movie_id and returns the name and role of the main character


def get_role_imdb(movie_id):
    movie_id = int(movie_id[2:])
    ia = imdb.IMDb()
    result = ia.get_movie(movie_id)
    if not ('cast' in result.keys()):
        return None, None
    if len(result['cast']) == 0:
        return None, None
    main_character = result['cast'][0]
    main_character_name = main_character.data['name']
    return main_character_name, str(main_character.currentRole)


# The function gets the crew list of a particular movie, and the name of the main character according to imdb,
# and returns according to tmdb its gender and its role


def get_gender_and_role_tmdb(movie_cast, character_name):
    for person in movie_cast:
        if (not ('known_for_department' in person.keys())) or person['known_for_department'] != 'Acting':
            return None, None
        if person['name'].casefold() == character_name.casefold():
            return person['gender'], person['character']
    return None, None
