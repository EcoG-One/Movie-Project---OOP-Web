import json

movies = {
    "The Shawshank Redemption": {
        "rating": 9.5,
        "year_of_release": 1994
    },
    "Pulp Fiction": {
        "rating": 8.8,
        "year_of_release": 1994
    },
    "The Room": {
        "rating": 3.6,
        "year_of_release": 2003
    },
    "The Godfather": {
        "rating": 9.2,
        "year_of_release": 1972
    },
    "The Godfather: Part II": {
        "rating": 9.0,
        "year_of_release": 1974
    },
    "The Dark Knight": {
        "rating": 9.0,
        "year_of_release": 2008
    },
    "12 Angry Men": {
        "rating": 9.0,
        "year_of_release": 1957
    },
    "Everything Everywhere All At Once": {
        "rating": 7.8,
        "year_of_release": 2022
    },
    "Forrest Gump": {
        "rating": 8.8,
        "year_of_release": 1994
    },
    "Star Wars: Episode V": {
        "rating": 8.7,
        "year_of_release": 1980
    }
}
dump_movies = json.dumps(movies)
with open('data.json', "w") as json_file:
    json_file.write(dump_movies)
json_file.close()