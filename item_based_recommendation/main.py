import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
movie = pd.read_csv(r"C:\Users\fesan\recommendation_system\datasets\movie_lens_dataset\movie.csv")
rating = pd.read_csv(r"C:\Users\fesan\recommendation_system\datasets\movie_lens_dataset\rating.csv")

movie.head()
rating.head()

df_merged = pd.merge(movie, rating, on='movieId',how="right")
rating_count = df_merged.movieId.value_counts().reset_index()
rating_count.columns = ["movieId", "rating_count"]

print(rating_count.head())

rare_movies = rating_count[rating_count["rating_count"] <= 1000]["movieId"]

common_movies = df_merged[~df_merged["movieId"].isin(rare_movies)]
common_movies.head()


user_movie_df = common_movies.pivot(index="userId", columns="movieId", values="rating")