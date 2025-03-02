from istorage import IStorage
import json

# We define colors as global variables
MAGENTA = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path


    def list_movies(self):
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
            with open(self.file_path, "r") as json_file:
                movies = json.loads(json_file.read())
            json_file.close()
        except IOError as e:
            print(RED, end=" ")
            print(e)
            print(ENDC, end=" ")
            print(GREEN + f"Do you want to create empty {self.file_path} file? \n"
                          f"Y : Create {self.file_path}\nN : Exit application " + ENDC)
            while True:
                choice = input('')
                if choice in ("Y", "y"):
                    movies = {}
                    self.save_movies(movies)
                    return movies
                elif choice in ("N", "n"):
                    exit()
                else:
                    print(BLUE + 'Please enter "Y" or "N"' + ENDC)
        return movies


    def save_movies(self, movies):
        """
        Gets all your movies as an argument and saves them to the JSON file.
        """
        dump_movies = json.dumps(movies)
        try:
            with open(self.file_path, "w") as json_file:
                json_file.write(dump_movies)
            json_file.close()
        except IOError as e:
            print(e)


    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.list_movies()
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster":poster
        }
        self.save_movies(movies)


    def delete_movie(self, title):
        """
            Deletes a movie from the movies database.
            Loads the information from the JSON file, deletes the movie,
            and saves it. The function doesn't need to validate the input.
            """
        movies = self.list_movies()
        if movies.pop(title, 0) == 0:  # checks if movie exists
            print(f"{RED}Movie '{title}' doesn't exist!{ENDC}")
        else:
            self.save_movies(movies)
            print(f'{MAGENTA}Movie "{title}" successfully deleted{ENDC}')


    def update_movie(self, title, rating):
        """
            Updates a movie from the movies database.
            Loads the information from the JSON file, updates the movie,
            and saves it. The function doesn't need to validate the input.
            """
        movies = self.list_movies()
        movies[title]["rating"] = rating
        self.save_movies(movies)

