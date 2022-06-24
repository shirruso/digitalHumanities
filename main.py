
from getGenderByWikidata import get_actors_per_country
import getOccupations
from getMoviesPerCountry import get_movies, countries
from getOccupations import create_occupations_array, open_all_json_files


if __name__ == '__main__':
    # get_actors_per_country(countries[0])
    # get_movies()
    create_occupations_array()
    getOccupations.open_all_json_files()

