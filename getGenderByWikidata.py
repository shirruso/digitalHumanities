from SPARQLWrapper import SPARQLWrapper, JSON


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.queryAndConvert()


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


def get_actor_gender(character_name, actors_list):
    for actor in actors_list:
        if character_name == actor[0]:
            return 0 if actor[1] == 'male' else 1
    return None
