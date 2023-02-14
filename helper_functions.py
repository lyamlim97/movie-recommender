# imports
import pandas as pd
import numpy as np

# function to calculate weighted rating
def calculate_weighted_rating(x, m, C):
    R = x['vote_average']
    v = x['vote_count']
    result = ((v / (v + m) * R)) + ((m / (v + m)) * C)
    return result


# function to return dataframe of top N movies for a particular genre
def top_N_movies(genre, N, df, percentile=0.9):
    df_specific_genre = df[df['genre'] == genre]

    min_votes = df_specific_genre['vote_count'].quantile(percentile)

    overall_average_rating = df_specific_genre['vote_average'].mean()

    df_movies_info_specific_genre_filtered = df_specific_genre[
        df_specific_genre['vote_count'] >= min_votes
    ]

    df_movies_info_specific_genre_filtered[
        'weighted_rating'
    ] = df_movies_info_specific_genre_filtered.apply(
        lambda x: calculate_weighted_rating(x, min_votes, overall_average_rating),
        axis=1,
    )

    df_movies_info_specific_genre_filtered = (
        df_movies_info_specific_genre_filtered.sort_values(
            'weighted_rating', ascending=False
        )
    )

    return df_movies_info_specific_genre_filtered[:N]


# function to take in a movie title as input and output the N most similar movies
def get_recommendations(title, N, indices, cosine_sim, df):
    # get index of the input movie
    index = indices[title]

    # get the similarity scores for all movies with the input movie
    scores = list(enumerate(cosine_sim[index]))

    # sort the movies based on the similarity scores
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # get the scores of the top N most similar movies
    scores = scores[1 : N + 1]

    # get the movie indices
    movie_indices = [i[0] for i in scores]

    # return the top N most similar movies
    result = df['title'].iloc[movie_indices]
    return result


# function to get the director name from the crew feature
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan


# function to get a list of the first 3 elements or entire list, whichever is more
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names

    return []


# function to convert all strings to lower case and strip name of spaces
def lower_and_strip_spaces(x):
    if isinstance(x, list):
        # for lists
        return [str.lower(i.replace(' ', '')) for i in x]
    elif isinstance(x, str):
        # for strings
        return str.lower(x.replace(' ', ''))
    else:
        return ''


# function to create metadata soup from the columns
def create_soup(x):
    return (
        ' '.join(x['keywords'])
        + ' '
        + ' '.join(x['cast'])
        + ' '
        + x['director']
        + ' '
        + ' '.join(x['genres'])
    )
