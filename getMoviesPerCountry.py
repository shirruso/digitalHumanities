import requests
import json
import imdb
from getGenderByWikidata import get_actors_per_country, get_actor_gender

keys = {'k_64p78757', 'k_ao1xicrn', 'k_cc9uodvl', 'k_sej8mhp2', 'k_ay2kvfye'}


class Country:
    def __init__(self, name, shortcut, language, wikidata_key, adjectival):
        self.name = name
        self.shortcut = shortcut
        self.language = language
        self.wikidata_key = wikidata_key
        self.adjectival = adjectival


countries = [
    # Country('Egypt', 'eg', 'ar', 'Q79', 'Egyptian'),
    # Country('Turkey', 'tr', 'tr', 'Q43', 'Turkish'),
    # Country('France', 'fr', 'fr', 'Q142', 'French'),
    # Country('Germany', 'de', 'de', 'Q183', 'German'),
    # Country('Italy', 'it', 'it', 'Q38', 'Italian'),
    # Country('United Kingdom', 'gb', 'en', 'Q145', 'British'),
    # Country('Greece', 'gr', 'el', 'Q41', 'Greek'),
    # Country('Poland', 'pl', 'pl', 'Q36', 'Polish'),
    # Country('Russia', 'ru', 'ru', 'Q159', 'Russian'),
    # Country('Japan', 'jp', 'ja', 'Q17', 'Japanese'),
    # Country('India', 'in', 'hi', 'Q668', 'Indian'),
    # Country('China', 'cn', 'zh', 'Q148', 'Chinese'),
    # Country('United States', 'us', 'en', 'Q30', 'American'),
    # Country('Mexico', 'mx', 'es', 'Q96', 'Mexican'),
    # Country('Canada', 'ca', 'en', 'Q16', 'Canadian'),
    # Country('Brazil', 'br', 'pt', 'Q155', 'Brazilian'),
    Country('Argentina', 'ar', 'es', 'Q414', 'Argentine'),
    # Country('Australia', 'au', 'en', 'Q408', 'Australian'),
    # Country('South Africa', 'za', 'af', 'Q258', 'South African'),

]

years = ['1960_1979', '1980_1999', '2000_2009', '2010_2012', '2013_2015', '2016_2018', '2019_2022']


def get_movies():
    for country in countries:
        get_movies_per_country(country)


# The function creates a json file which contains all the movies of a particular country according to the years in
# 'years' array
def get_movies_per_country(country):
    json_dict = {}
    actors_list = get_actors_per_country(country)
    for years_range in years:
        json_dict.update({years_range: get_movies_per_years(country, years_range, actors_list)})
    path = './json files/%s.json' % country.name
    with open(path, 'w') as outfile:
        json.dump(json_dict, outfile, indent=4)


def get_movies_by_pages(country, years_range):
    movies = []
    num_of_pages = 3
    release_data_from, release_data_to = years_range[0:4], years_range[5:]
    for i in range(0, num_of_pages):
        query = 'https://imdb-api.com/API/AdvancedSearch/k_ay2kvfye?title_type=feature,tv_movie,short,' \
                'tv_short&release_date=%s-01-01,' \
                '%s-12-31&countries=%s&languages=%s&count=250&start=%d' % (
                    release_data_from, release_data_to, country.shortcut,
                    country.language, i * 250 + 1)
        response = requests.get(query)
        response_json = response.json()
        movies_per_page = response_json['results']
        movies.append(movies_per_page)
    flat_movies = [movie for sublist in movies for movie in sublist]
    return flat_movies


# The function returns an array of movies that have been released over the years. The array contains for each movie
# its id as well as its title.
def get_movies_per_years(country, years_range, actors_list):
    movies = get_movies_by_pages(country, years_range)
    filtered_movies = []
    for movie in movies:
        main_character_name, role_from_imdb = get_name_and_role_imdb(movie['id'])
        if main_character_name is None:
            continue
        gender_by_wikidata = get_actor_gender(main_character_name, actors_list)
        response = requests.get('https://api.themoviedb.org/3/movie/%s/credits?api_key=dafbfad599cde5d98a5d1c68cef38b1c'
                                % movie['id'])
        response_json = response.json()
        if (not response.ok) or len(response_json['cast']) == 0:
            if gender_by_wikidata is None:
                continue
            data = get_data(movie['id'], movie['title'], movie['description'][1:-1], movie['plot'], main_character_name,
                            gender_by_wikidata, '', role_from_imdb)
            filtered_movies.append(data)
            continue
        gender_by_tmdb, role_from_tmdb = get_gender_and_role_tmdb(response_json['cast'], main_character_name)
        gender = gender_by_wikidata if gender_by_wikidata is not None else gender_by_tmdb
        if gender is None or gender == 2:
            continue
        data = get_data(movie['id'], movie['title'], movie['description'][1:-1], movie['plot'], main_character_name,
                        gender, role_from_tmdb, role_from_imdb)
        filtered_movies.append(data)
    return filtered_movies


def get_data(movie_id, title, release_year, plot, main_character_name, main_character_gender, role_from_imdb,
             role_from_tmdb):
    return {'id': movie_id,
            'title': title,
            'release_year': release_year,
            'plot': plot,
            'main_character_name': main_character_name,
            'main_character_gender': main_character_gender,
            'main_character_role': [role_from_imdb, role_from_tmdb]}


# The function receives movie_id and returns the name and role of the main character
def get_name_and_role_imdb(movie_id):
    movie_id = int(movie_id[2:])
    try:
        ia = imdb.IMDb()
        result = ia.get_movie(movie_id)
    except:
        return None, None
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
            return None, ''
        if person['name'].casefold() == character_name.casefold():
            return person['gender'], person['character']
    return None, ''
