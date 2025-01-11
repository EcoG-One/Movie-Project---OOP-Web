import statistics
import random
import matplotlib.pyplot as plt
from thefuzz import process

# We define colors as global variables
MAGENTA = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'


def list_movies(movies):
    '''
        Prints all the movies, along with their rating and their total.
    '''
    print(f'{len(movies)} movies in total')
    for movie, properties in movies.items():
        print(f'{movie} ({properties["year_of_release"]}): {properties["rating"]}')

def add_movie(movies):
    '''
        Adds the movie name and properties that the user inputs
    '''
    movie_title = input(GREEN + 'Enter new movie name: ')
    movie_year_of_release = int(input('Enter new movie year: '))
    movie_rating = float(input('Enter new movie rating (0-10): '))
    movie_properties = {
            "rating": movie_rating,
            "year_of_release": movie_year_of_release
            }
    movies[movie_title] = movie_properties
    print(f'Movie {movie_title} successfully added{ENDC}')

def delete_movie(movies):
    '''
        Deletes the movie that the user inputs
    '''
    movie_title = input(GREEN + 'Enter movie name to delete: ' + ENDC)
    if movies.pop(movie_title, 0) == 0: #checks if movie exists
        print(f"{RED}Movie {movie_title} doesn't exist!{ENDC}")
    else:
        print(f'Movie {movie_title} successfully deleted')

def update_movie(movies):
    '''
        If the movie that the user entered exists, it updates the movie’s rating
    '''
    movie_title = input(GREEN + 'Enter movie name: ' + ENDC)
    if movies.get(movie_title, 0) == 0:     #checks if movie exists
        print(f"{RED}Movie {movie_title} doesn't exist!{ENDC}")
    else:
        new_movie_rate = float(input(GREEN + "Enter new movie rating (0-10): " + ENDC))
        movies[movie_title]["rating"] = new_movie_rate
        print(f'Movie {movie_title} successfully updated')


def stats(movies):
    '''
        Prints statistics about the movies in the database, (Average, Median, Best, Worst), using the statistics library
    '''
    rate = []
    for properties in movies.values():
        rate.append(properties["rating"])
    print(f'Average rating: {statistics.mean(rate)}')
    print(f'Median rating: {statistics.median(rate)}')
    sorted_movies = sorted(movies.items(), key = lambda movie_rate : movie_rate[1]["rating"])
    print(f'Best movie: {sorted_movies[-1][0]}, {max(rate)}')
    print(f'Worst movie: {sorted_movies[0][0]}, {min(rate)}')

def random_movie(movies):
    '''
        Prints a random movie and it’s rating, using the random library
    '''
    rand_movie = random.choice(list(movies.keys()))
    print(f"Your movie for tonight: {GREEN}{rand_movie}{ENDC}, it's rated {GREEN}{movies[rand_movie]['rating']}{ENDC}")

def search_movie(movies):
    '''
        Prints all the movies that matched the user’s query, along with the rating.
        If no movie is found, it uses fuzzy logic to suggest similar movies, using the thefuzz library
    '''
    name = input(GREEN + "Enter part of movie name: " + ENDC)
    count = 0
    for movie_title in list(movies.keys()):
        if name.lower() in movie_title.lower():   # search must be case insensitive
            print(f'{movie_title}, {movies[movie_title]["rating"]}')
            count +=1
    if count == 0:
        fuzzy_movies = process.extract(name, list(movies.keys()))
        closest_fuzzy_movies = [result for result in fuzzy_movies if result[1] >= 60] # We define the fuzzy matching
        if not closest_fuzzy_movies:                                                # threshold as 60%
            print(f'{RED}The movie {name} does not exist.{ENDC}')
        else:
            print(f'{RED}The movie {name} does not exist.{ENDC} Did you mean:')
            for fuzzy_movie in closest_fuzzy_movies:
                print(fuzzy_movie[0])   

def sort_movies_by_rating(movies):
    '''
        Prints all the movies and their ratings, in a descending order by the rating
    '''
    sorted_movies = sorted(movies.items(), key = lambda movie_rate : movie_rate[1]["rating"], reverse=True)
    for sorted_movie in sorted_movies:
        print(f'{sorted_movie[0]} ({sorted_movie[1]["year_of_release"]}): {sorted_movie[1]["rating"]}')

def sort_movies_by_year(movies):
    '''
        Prints all the movies and their ratings, in a descending order by the rating
    '''
    while True:
        choice = input(GREEN + "Do you want the latest movies first?  (Y/N) " + ENDC)
        if choice in ("Y", "y"):
            rev = True
            break
        elif choice in ("N", "n"):
            rev = False
            break
        else:
            print('Please enter "Y" or "N"')
    sorted_movies = sorted(movies.items(), key = lambda movie_rate : movie_rate[1]["year_of_release"], reverse=rev)
    for sorted_movie in sorted_movies:
        print(f'{sorted_movie[0]} ({sorted_movie[1]["year_of_release"]}): {sorted_movie[1]["rating"]}')


def create_histogram(movies):
    '''
        Creates an histogram of the ratings of the movies, using the matplotlib library
    '''
    rate = []
    for properties in movies.values():
        rate.append(properties["rating"])
    plt.hist(rate)
    plt.title("Movies Ratings")
    plt.xlabel("Rate")
    plt.ylabel("Movies")
    save_file = input(GREEN + "Histogram created successfully.\nPlease enter a file name to save it: " + ENDC)
    try:
        plt.savefig(save_file + '.png')
    except IOError as e:
        print(e)
    else:
        print(GREEN + "Histogram saved successfully." + ENDC)
    plt.show()      # we can comment out this line, if we don't want to display the histogram
    plt.close

def input_validation(num):
  while True:
    try:
        num = int(num)
    except ValueError:
        num = input(f"{GREEN}'{num}'{RED} is not a Number. Please enter a Number (0 to 10): {ENDC}")
    else:
        return num


def main():
      # Dictionary of Dictionaries to store the movies and their properties
    movies = {
        "The Shawshank Redemption": {
            "rating": 9.5,
            "year_of_release": 1994
        },
        "Pulp Fiction":  {
            "rating": 8.8,
            "year_of_release": 1994
        },
        "The Room":  {
            "rating": 3.6,
            "year_of_release": 2003
        },
        "The Godfather":  {
            "rating": 9.2,
            "year_of_release": 1972
        },
        "The Godfather: Part II":  {
            "rating": 9.0,
            "year_of_release": 1974
        },
        "The Dark Knight":  {
            "rating": 9.0,
            "year_of_release": 2008
        },
        "12 Angry Men":  {
            "rating": 9.0,
            "year_of_release": 1957
        },
        "Everything Everywhere All At Once":  {
            "rating": 7.8,
            "year_of_release": 2022
        },
        "Forrest Gump":  {
            "rating": 8.8,
            "year_of_release": 1994
        },
        "Star Wars: Episode V":  {
            "rating": 8.7,
            "year_of_release": 1980
        }
    }
    print(MAGENTA + '\033[4m' + '********** My Movies Database **********\n' + ENDC)
    # list of choices to use in menu selection
    choices = ['break', 'list_movies', 'add_movie', 'delete_movie', 'update_movie', 'stats', 'random_movie',
               'search_movie', 'sort_movies_by_rating', 'sort_movies_by_year', 'create_histogram']
    while True:
        choice = input(BLUE + "Menu:\n0. Quit\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie\n"
                              "5. Stats\n6. Random movie\n7. Search movie\n8. Movies sorted by rating\n"
                              "9. Movies sorted by year\n10. Create Rating Histogram\n\nEnter choice (0-10): " + ENDC)
        choice = input_validation(choice)
        if choice == 0:
            print(GREEN +"Bye!" + ENDC)
            break
        print("")
        if int(choice) not in range(11):
            print(RED + "Invalid choice\n" + ENDC)
        else:     # using the function exec to avoid the 11 loops needed for menu selection
            exec(f'{choices[int(choice)]}(movies)')
            input(BLUE + "\nPress enter to continue" + ENDC)


if __name__ == '__main__': 
    main()