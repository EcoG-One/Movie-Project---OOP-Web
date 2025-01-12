import json


# We define colors as global variables
MAGENTA = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'



def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    try:
        with open('data.json', "r") as json_file:
            movies = json.loads(json_file.read())
        json_file.close()
    except IOError as e:
        print(e)
    else:
        return movies

def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    dump_movies = json.dumps(movies)
    try:
        with open('data.json', "w") as json_file:
            json_file.write(dump_movies)
        json_file.close()
    except IOError as e:
        print(e)



def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title] = {
        "year": year,
        "rating": rating
    }
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    if movies.pop(title, 0) == 0:  # checks if movie exists
        print(f"{RED}Movie {title} doesn't exist!{ENDC}")
    else:
        save_movies(movies)
        print(f'Movie {title} successfully deleted')


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title]["rating"] = rating
    save_movies(movies)
  