"""
Main entry point for the Movie App.

Initializes the application with the chosen storage (JSON or CSV)
and runs the menu-driven interface for managing the movie database
"""
from movie_app import MovieApp
# from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson

# storage = StorageCsv("data/movies.csv")
storage = StorageJson("data/movies.json")
movie_app = MovieApp(storage)
movie_app.run()
