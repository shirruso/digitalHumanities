import json
from SPARQLWrapper import SPARQLWrapper, JSON
from getMoviesPerCountry import countries, years

occupations = []


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


# The function uses a wikidata query to create an array of occupations.
def create_occupations_array():
    endpoint_url = "https://query.wikidata.org/sparql"
    query = """SELECT ?occLabel  WHERE {
                ?occ wdt:P31 wd:Q28640.   
                 SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                }
             """
    results = get_results(endpoint_url, query)
    for result in results["results"]["bindings"]:
        if not result["occLabel"]["value"][1:].isnumeric():
            occupations.append(result["occLabel"]["value"])


# The function checks whether A is a subset of X
def is_a_in_x(a, x):
    for i in range(len(x) - len(a) + 1):
        if a == x[i:i + len(a)]:
            return True
    return False


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
        role_by_imdb_and_tmdb = movie['main_character_role']
        occupation = find_character_occupation(role_by_imdb_and_tmdb)
        if occupation is None:
            continue
        movie['main_character_role'] = occupation
        updated_movies_arr.append(movie)
    return updated_movies_arr


def find_character_occupation(role_by_imdb_and_tmdb):
    for occupation in occupations:
        imdb_role_arr = role_by_imdb_and_tmdb[0].lower().split(' ')
        tmdb_role_arr = role_by_imdb_and_tmdb[1].lower().split(' ')
        occupation_arr = occupation.lower().split(' ')
        if (len(imdb_role_arr) >= len(occupation_arr) and is_a_in_x(occupation_arr, imdb_role_arr)) or (
                len(tmdb_role_arr) >= len(occupation_arr) and is_a_in_x(occupation_arr, tmdb_role_arr)):
            return occupation
    return None
