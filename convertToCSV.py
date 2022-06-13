import csv
import json

def open_all_json_files():
    header = ['title', 'release_year', 'main_character_name', 'main_character_gender', 'main_character_role']
    data = []
    path = 'Egypt.json'
    with open(path, 'r') as json_file:
        movies_per_country = json.load(json_file)
        for years_range, movies_arr in movies_per_country.items():
            for movie in movies_arr:
                movie_arr = [movie['title'],
                             movie['release_year'],
                             movie['main_character_name'],
                             movie['main_character_gender'],
                             movie['main_character_role']]
                data.append(movie_arr)
    with open('Egypt.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        # write the header
        writer.writerow(header)
        # write multiple rows
        writer.writerows(data)

open_all_json_files()
