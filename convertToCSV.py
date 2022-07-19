import csv
import json
import pandas as pd


def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False


def sub_release_year(release_year):
    i = 0
    for character in release_year:
        if character.isdigit():
            return release_year[i:]
        i += 1


def open_all_json_files(country):
    header = ['title', 'release_year', 'main_character_name', 'main_character_gender', 'country', 'main_character_role']
    data = []
    path = 'json_files/%s.json' % country
    with open(path, 'r') as json_file:
        movies_per_country = json.load(json_file)
        for years_range, movies_arr in movies_per_country.items():
            for movie in movies_arr:
                if not movie['release_year'].isdigit():
                    release_year_arr = movie['release_year'].split(' ')
                    for word in release_year_arr:
                        if containsNumber(word):
                            release_year = word
                    if not release_year.isdigit():
                        release_year = sub_release_year(release_year)
                else:
                    release_year = movie['release_year']
                if movie['main_character_gender'] == 0:
                    gender = "Male"
                else:
                    gender = "Female"
                movie_arr = [movie['title'],
                             release_year,
                             movie['main_character_name'],
                             gender,
                             country,
                             movie['main_character_role']]
                data.append(movie_arr)
    with open('csv_files/%s.csv' % country, 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        # write the header
        writer.writerow(header)
        # write multiple rows
        writer.writerows(data)


def combine_all_csv():
    all_filenames = ['csv_files/%s.csv' % country for country in countries]
    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # export to csv
    combined_csv.to_csv("csv_files/combined_csv.csv", index=False, encoding='utf-8-sig')


countries = ['Argentina', 'Australia', 'Brazil', 'Canada', 'Egypt', 'France', 'Germany',
             'Greece', 'India', 'Italy', 'Japan', 'Mexico', 'Poland', 'Russia',
             'South Africa', 'Turkey', 'United Kingdom', 'United States']

for country in countries:
    open_all_json_files(country)

combine_all_csv()