import json
import numpy as np
import wikipedia
from SPARQLWrapper import SPARQLWrapper, JSON
from getMoviesPerCountry import countries, years

occupations = ['football player', 'bank manger', 'computer system analyst']

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


# The function uses a wikidata query to create an array of occupations.
def create_occupations_array():
    res = []
    endpoint_url = "https://query.wikidata.org/sparql"
    query = """SELECT ?occLabel  WHERE {
                ?occ wdt:P31 wd:Q28640.   
                 SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                }
             """
    results = get_results(endpoint_url, query)
    for result in results["results"]["bindings"]:
        if not result["occLabel"]["value"][1:].isnumeric():
            occupation = result["occLabel"]["value"]
            res.append(occupation.lower())
            sub_occupations = get_sub_occupations(occupation)
            res.extend(sub_occupations)

    # deleting duplicates
    [occupations.append(x) for x in res if x not in occupations]

    my_file = open("bad_occ.txt", "r")
    bad_occ = my_file.read()
    bad_occ_list = bad_occ.split('\n')
    my_file.close()

    diff = list(set(occupations).difference(set(bad_occ_list)))
    occupations.clear()
    occupations.extend(diff)
    print(occupations)


def get_sub_occupations(occupation):
    new_occupation = []
    professions_suffix = ['er', 'or', 'ist', 'ian', 'ant', 'man', 'ee']
    occupation_arr = occupation.split(' ')
    for suffix in professions_suffix:
        for sub_occ in occupation_arr:
            if sub_occ.endswith(suffix):
                new_occupation.append(sub_occ.lower())
    return new_occupation


# The function checks whether A is a subset of X
def is_a_in_x(a, x):
    for i in range(len(x) - len(a) + 1):
        if a == x[i:i + len(a)]:
            return True
    return False


# For each movie that exists in a json file, the function finds the role of the main character.
# Then, rewrites to the file the role of the character.
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
        occupation = get_character_occupation(movie)
        if occupation:
            movie['main_character_role'] = occupation
            updated_movies_arr.append(movie)
    return updated_movies_arr


# Given a movie, the function seeks out the role of the main character in several ways.
def get_character_occupation(movie_desc):
    # option 1 : if the character's role is written in the json file in the field: 'main_character_role'
    role_by_imdb_and_tmdb = movie_desc['main_character_role']
    imdb_role = role_by_imdb_and_tmdb[0]
    tmdb_role = role_by_imdb_and_tmdb[1]
    if not (occupation := get_character_occupation_by_sentence(imdb_role)):
        occupation = get_character_occupation_by_sentence(tmdb_role)
    if occupation:
        return occupation

    # option 2: if the role of the character is written in the plot.
    # The plot is accepted by imdb or by wikipedia.
    plot_by_wiki = get_plot(movie_desc['title'], movie_desc['release_year'])
    plot_by_imdb = movie_desc['plot']
    names_and_plots = [[imdb_role, plot_by_imdb],
                       [tmdb_role, plot_by_imdb],
                       [imdb_role, plot_by_wiki],
                       [tmdb_role, plot_by_wiki]]
    for name_and_plot in names_and_plots:
        if occupation := get_occupation_by_plot(name_and_plot[0], name_and_plot[1]):
            return occupation
    return None


def get_character_occupation_by_sentence(sentence):
    if (sentence is None) or len(sentence) == 0:
        return None
    for occupation in occupations:
        sentence_arr = sentence.lower().split(' ')
        occupation_arr = occupation.lower().split(' ')
        if len(sentence_arr) >= len(occupation_arr) and is_a_in_x(occupation_arr, sentence_arr):
            return occupation
    return None


def get_plot(film_name, year):
    possibles = ['Plot', 'Synopsis', 'Plot synopsis', 'Plot summary',
                 'Story', 'Plotline', 'The Beginning', 'Summary',
                 'Content', 'Premise']
    possibles_edit = [i + 'Edit' for i in possibles]
    all_possibles = possibles + possibles_edit
    film_names = [film_name + ' ' + '(' + year + ' film)', film_name + '(' + year + ')', film_name + ' (film)',
                  film_name]
    plot = None
    for j in film_names:
        try:
            page = wikipedia.WikipediaPage(j)
            if page:
                break
        except:
            page = None

    try:
        for j in all_possibles:
            if page.section(j) is not None:
                plot = page.section(j).replace('\n', '').replace("\'", "")
    except:
        print('error occurred')
        plot = None

    return plot


def get_occupation_by_plot(character_name, plot):
    if (character_name is None) or len(character_name) == 0 or plot is None:
        return None
    character_sentences = get_sentences_in_plot_contain_character(character_name, plot)
    for sentence in character_sentences:
        occupation = get_character_occupation_by_sentence(sentence)
        if occupation:
            return occupation
    return None


def get_sentences_in_plot_contain_character(character_name, plot):
    sentences_character_appears_in = []
    if plot:
        sentences_character_appears_in = [sentence.lower().replace(',', '')
                                          for sentence in plot.split('.')
                                          if any([character_name.lower() in sentence.lower()])]
    return sentences_character_appears_in
