from SPARQLWrapper import SPARQLWrapper, JSON


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def get_actors_per_country(country):
    endpoint_url = "https://query.wikidata.org/sparql"
    query = """
            SELECT ?personLabel ?genderLabel
            WHERE
            {
                   ?person wdt:P31 wd:Q5 .
                   ?person wdt:P106 wd:Q33999 .
                   ?person wdt:P27 wd:%s .
                   ?person wdt:P21 ?gender .
            
                   SERVICE wikibase:label {bd:serviceParam wikibase:language "en" }
            }
    """ % country.wikidata_key

    actors_and_gender = []
    results = get_results(endpoint_url, query)
    for result in results["results"]["bindings"]:
        if not result["personLabel"]["value"][1:].isnumeric():
            actors_and_gender.append([result["personLabel"]["value"], result["genderLabel"]["value"]])
    return actors_and_gender

#
# def open_all_json_files():
#     for country in countries:
#         actors_list = get_actors_per_country(country)
#         path = './json files/%s.json' % country.name
#         with open(path, 'r') as json_file:
#             movies_per_country = json.load(json_file)
#             json_dict = {}
#             for years_range, movies_arr in movies_per_country.items():
#                 updated_movies_arr = update_character_gender(movies_arr, actors_list)
#                 json_dict.update({years_range: updated_movies_arr})
#         with open(path, 'w') as outfile:
#             json.dump(json_dict, outfile, indent=4)
#
#
# def update_character_gender(movies_arr, actors_list):
#     updated_movies_arr = []
#     for movie in movies_arr:
#         if movie['main_character_gender'] == 2:
#             gender_by_wikidata = get_actor_gender(movie['main_character_name'], actors_list)
#             if gender_by_wikidata is not None:
#                 movie['main_character_gender'] = gender_by_wikidata
#                 updated_movies_arr.append(movie)
#         else:
#             updated_movies_arr.append(movie)
#     return updated_movies_arr


def get_actor_gender(character_name, actors_list):
    for actor in actors_list:
        if character_name == actor[0]:
            return 0 if actor[1] == 'male' else 1
    return None
