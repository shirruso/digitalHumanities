import config
import requests
from getMoviesPerCountry import get_movies_per_country, countries
from getOccupations import create_occupations_array, open_all_json_files
if __name__ == '__main__':
    # get_movies_per_country(countries[0])

    create_occupations_array()
    open_all_json_files()
