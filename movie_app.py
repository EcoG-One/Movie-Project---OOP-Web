import statistics
import random
import matplotlib.pyplot as plt
from thefuzz import process
import requests
from dotenv import load_dotenv
import os

# We define colors as global variables
MAGENTA = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'

load_dotenv()

class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self):
        """
        Prints all the movies, along with their rating and their total.
        """
        movies = self._storage.list_movies()
        print(f'{len(movies)} movies in total')
        for movie, properties in movies.items():
            print(f'{movie} ({properties["year"]}): {properties["rating"]}')

    def _command_add_movie(self):
        """
        Adds the movie that the user inputs and gets it's properties
        from the omdb API
        """
        movies = self._storage.list_movies()
        while True:
            title = input(GREEN + 'Enter new movie name: ')
            if title != '':
                break
        if title in movies:
            print(f"{MAGENTA}Movie {title} already exist!{ENDC}")
            return

        URL = 'http://www.omdbapi.com/?'
        APIKEY = os.getenv('apikey')
        param = {'apikey':APIKEY, 't':title}
        try:
            movie_res = requests.get(URL, params=param)
        except requests.exceptions.RequestException as e:
            print(e)
            return
        movie_data = movie_res.json()
        if movie_data == {"Response":"False","Error":"Movie not found!"}:
            print("Error: Movie not found!")
        else:
            try:
                self._storage.add_movie(title,
                            int(movie_data.get("Year", 1900)),
                            float(movie_data.get("imdbRating", 0)),
                            movie_data.get("Poster", "N/A"))
                print(f'{MAGENTA}Movie "{title}" successfully added{ENDC}')
            except ValueError:
                print("Error: omdb returned invalid data")

    def _command_delete_movie(self):
        """
        Deletes the movie that the user inputs
        """
        while True:
            title = input(GREEN + 'Enter movie name to delete: ' + ENDC)
            if title != '':
                break
        self._storage.delete_movie(title)

    def _command_update_movie(self):
        """
        If the movie that the user entered exists,
        it updates the movie’s rating
        """
        movies = self._storage.list_movies()
        while True:
            title = input(GREEN + 'Enter movie name: ' + ENDC)
            if title != '':
                break
        if movies.get(title, 0) == 0:  # checks if movie exists
            print(f"{RED}Movie {title} doesn't exist!{ENDC}")
        else:
            rating = self.float_validation(
                input(GREEN + "Enter new movie rating (0-10): " + ENDC))
            self._storage.update_movie(title, rating)
            print(f'{MAGENTA}Movie "{title}" successfully '
                  f'updated with a new rating of: {rating} !{ENDC}')

    def _command_movie_stats(self):
        """
        Prints statistics about the movies in the database,
        (Average, Median, Best, Worst), using the statistics library
        """
        movies = self._storage.list_movies()
        if movies == {}:
            print(RED + "No movies in database" + ENDC)
            return
        rate = []
        for properties in movies.values():
            rate.append(properties["rating"])
        print(f'Average rating: {statistics.mean(rate):.1f}')
        print(f'Median rating: {statistics.median(rate):.1f}')
        sorted_movies = sorted(movies.items(),
                               key=lambda movie_rate: movie_rate[1]["rating"])
        print(f'Best movie: {sorted_movies[-1][0]}, {max(rate)}')
        print(f'Worst movie: {sorted_movies[0][0]}, {min(rate)}')

    def _command_random_movie(self):
        """
        Prints a random movie and it’s rating, using the random library
        """
        movies = self._storage.list_movies()
        if movies == {}:
            print(RED + "No movies in database" + ENDC)
            return
        rand_movie = random.choice(list(movies.keys()))
        print(
            f"Your movie for tonight: {GREEN}{rand_movie}{ENDC}, "
            f"it's rated {GREEN}{movies[rand_movie]['rating']}{ENDC}")

    def _command_search_movie(self):
        """
        Prints all the movies that matched the user’s query,
        along with the rating.
        If no movie is found, it uses fuzzy logic to suggest
        similar movies, using the thefuzz library
        """
        movies = self._storage.list_movies()
        if movies == {}:
            print(RED + "No movies in database" + ENDC)
            return
        name = input(GREEN + "Enter part of movie name: " + ENDC)
        count = 0
        for title in list(movies.keys()):
            if name.lower() in title.lower(): # search must be case-insensitive
                print(f'{title}, {movies[title]["rating"]}')
                count += 1
        if count == 0:
            fuzzy_movies = process.extract(name, list(movies.keys()))
            closest_fuzzy_movies = [result for result in fuzzy_movies if
                                    result[
                                        1] >= 60] # Define the fuzzy matching
            if not closest_fuzzy_movies:  # threshold as 60%
                print(f'{RED}The movie {name} does not exist.{ENDC}')
            else:
                print(
                    f'{RED}The movie {name} does not exist.{ENDC} '
                    f'Did you mean:')
                for fuzzy_movie in closest_fuzzy_movies:
                    print(fuzzy_movie[0])

    def _command_sort_movies_by_rating(self):
        """
        Prints all the movies and their ratings,
        in descending order by the rating
        """
        movies = self._storage.list_movies()
        if movies == {}:
            print(RED + "No movies in database" + ENDC)
            return
        sorted_movies = sorted(movies.items(),
                               key=lambda movie_rate: movie_rate[1]["rating"],
                               reverse=True)
        for sorted_movie in sorted_movies:
            print(
                f'{sorted_movie[0]} ({sorted_movie[1]["year"]}): '
                f'{sorted_movie[1]["rating"]}')

    def _command_sort_movies_by_year(self):
        """
        Prints all the movies and their ratings,
        in descending order by the rating
        """
        movies = self._storage.list_movies()
        if movies == {}:
            print(RED + "No movies in database" + ENDC)
            return
        while True:
            choice = input(
                GREEN + "Do you want the latest movies first?  (Y/N) " + ENDC)
            if choice in ("Y", "y"):
                rev = True
                break
            elif choice in ("N", "n"):
                rev = False
                break
            else:
                print('Please enter "Y" or "N"')
        sorted_movies = sorted(movies.items(),
                               key=lambda movie_rate: movie_rate[1]["year"],
                               reverse=rev)
        for sorted_movie in sorted_movies:
            print(
                f'{sorted_movie[0]} ({sorted_movie[1]["year"]}): '
                f'{sorted_movie[1]["rating"]}')

    def _command_create_histogram(self):
        """
        Creates a histogram of the ratings of the movies,
        using the matplotlib library
        """
        movies = self._storage.list_movies()
        if movies == {}:
            print(RED + "No movies in database" + ENDC)
            return
        rate = []
        for properties in movies.values():
            rate.append(properties["rating"])
        plt.hist(rate)
        plt.title("Movies Ratings")
        plt.xlabel("Rate")
        plt.ylabel("Movies")
        save_file = input(
            GREEN + "Histogram created successfully."
                    "\nPlease enter a file name to save it: " + ENDC)
        try:
            plt.savefig(save_file + '.png')
        except IOError as e:
            print(e)
        else:
            print(GREEN + "Histogram saved successfully." + ENDC)
      #  plt.show()  we can add this line, if we want to display the histogram
        plt.close()

    def _command_filter_movies(self):
        """
        Filters the list of movies based on minimum rating,
        start year and end year
        """
        movies = self._storage.list_movies()
        if movies == {}:
            print(RED + "No movies in database" + ENDC)
            return
        min_rate = input(
            "Enter minimum rating (leave blank for no minimum rating): ")
        if min_rate != '':
            min_rate = self.float_enter_validation(min_rate)
        start = input("Enter start year (leave blank for no start year): ")
        if start != '':
            start = self.int_enter_validation(start)
        end = input("Enter end year (leave blank for no end year): ")
        if end != '':
            end = self.int_enter_validation(end)
        if min_rate != '':
            movies = {key: value for key, value in movies.items() if
                      value["rating"] >= min_rate}
        if start != '':
            movies = {key: value for key, value in movies.items() if
                      value["year"] >= start}
        if end != '':
            movies = {key: value for key, value in movies.items() if
                      value["year"] <= end}
        if len(movies) > 0:
            print("Filtered Movies:")
            for movie, properties in movies.items():
                print(
                    f'{movie} ({properties["year"]}): {properties["rating"]}')
        else:
            print(
                MAGENTA + "No movies found based on the provided criteria"
                + ENDC)

    def int_validation(self, num):
        """
        Validates if input string is an integer
        and returns it as an integer
        :param num: string
        :return: integer
        """
        while True:
            try:
                num = int(num)
            except ValueError:
                num = input(
                    f"{GREEN}'{num}'{RED} is not an Integer Number. "
                    f"Please enter an Integer: {ENDC}")
            else:
                return num

    def int_enter_validation(self, num):
        """
        Validates if input string is an integer or ''
        and returns it as an integer or ''
        :param num: string
        :return: integer or ''
        """
        while True:
            try:
                num = int(num)
            except ValueError:
                if num == '':
                    return num
                num = input(
                    f"{GREEN}'{num}'{RED} is not an Integer Number. "
                    f"Please enter an Integer: {ENDC}")
            else:
                return num

    def float_validation(self, num):
        """
        Validates if input string is a floating
        and returns it as a floating
        :param num: string
        :return: floating number
        """
        while True:
            try:
                num = float(num)
                if num > 10:
                    num = 10
                    print(f"{MAGENTA}You entered a Number grater than 10. "
                          f"Your new rating will be 10.{ENDC}")
            except ValueError:
                num = input(
                    f"{GREEN}'{num}'{RED} is not a Number. "
                    f"Please enter a Number (0 to 10): {ENDC}")
            else:
                return num

    def float_enter_validation(self, num):
        """
        Validates if input string is a floating or ''
        and returns it as a floating or ''
        :param num: string
        :return: floating number or ''
        """
        while True:
            try:
                num = float(num)
            except ValueError:
                if num == '':
                    return num
                num = input(
                    f"{GREEN}'{num}'{RED} is not a Number. "
                    f"Please enter a Number: {ENDC}")
            else:
                return num

    def serialize_movie(self, movie, properties):
        '''
        Serializes a movie object and outputs it as HTML
        :param movie: Dictionary of the movie
        :param properties: Dictionary with the movie properties
        :return: the movie object as HTML
        '''
        output = ''
        try:
            output += (f'        <li>\n'
                       f'            <div class="movie">\n'
                       f'                <img class="movie-poster" '
                       f'src={properties["poster"]} title=""/>\n'
                       f'                <div class ="movie-title">{movie}'
                       f'</div>\n'
                       f'                <div class ="movie-year">'
                       f'{properties["year"]}</div>\n'
                       f'            </div>\n'
                       f'        </li>\n'
                       )
        except (KeyError, IndexError):
            pass
        return output

    def read_data(self):
        '''
        Iterates through the objects of movies list, adding them
            to the HTML using the serialize_movie() function
        :return: all movies properties as HTML
        '''
        movies = self._storage.list_movies()
        output = '\n'
        for movie, properties in movies.items():
            output += self.serialize_movie(movie, properties)
        return output

    def read_html(self):
        '''
        Reads the HTML template file
        :return: the HTML template as string
        '''
        try:
            with open("_static\index_template.html", "r") as html_template:
                return html_template.read()
        except IOError as e:
            print(f'WARNING! {e}. Exiting...')
            exit()

    def _command_generate_website(self):
        '''
        Generates the website according to the template,
        and creates a file called index.html that has the full website
        '''
        new_html = self.read_html().replace("__TEMPLATE_MOVIE_GRID__",
                                       self.read_data())
        try:
            with open("_static\index.html", "w") as new_html_file:
                new_html_file.write(new_html)
            print("Website was generated successfully.")
        except IOError as e:
            print(f'WARNING! {e}. Exiting...')
            exit()

    def _command_bye_bye(self):
        '''
        Exits the application
        '''
        print(GREEN + "Bye!" + ENDC)
        exit()

    def run(self):
        """
        main function, creates menu of choices and navigates to them
        """
        print(
            MAGENTA + '\033[4m' + '********** My Movies Database **********\n'
            + ENDC)
        # Dictionary of choices to use in menu selection
        choices = {
            0: self._command_bye_bye,
            1: self._command_list_movies,
            2: self._command_add_movie,
            3: self._command_delete_movie,
            4: self._command_update_movie,
            5: self._command_movie_stats,
            6: self._command_random_movie,
            7: self._command_search_movie,
            8: self._command_sort_movies_by_rating,
            9: self._command_sort_movies_by_year,
            10: self._command_create_histogram,
            11: self._command_filter_movies,
            12: self._command_generate_website
        }
        while True:
            choice = input(
                BLUE + "Menu:\n"
                       "0. Quit\n"
                       "1. List movies\n"
                       "2. Add movie\n"
                       "3. Delete movie\n"
                       "4. Update movie\n"
                       "5. Stats\n"
                       "6. Random movie\n"
                       "7. Search movie\n"
                       "8. Movies sorted by rating\n"
                       "9. Movies sorted by year\n"
                       "10. Create Rating Histogram\n"
                       "11. Filter Movies\n"
                       "12. Generate Website\n\n"
                       "Enter choice (0-12): " + ENDC)
            choice = self.int_validation(choice)
            print("")
            if choice not in range(13):
                print(RED + "Invalid choice\n" + ENDC)
            else:
                choices[choice]()
                input(BLUE + "\nPress enter to continue" + ENDC)
