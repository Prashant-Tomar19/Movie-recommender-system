import streamlit as st
import pickle
import pandas as pd
import requests
import gzip

import os

API_KEY = os.getenv("TMDB_API_KEY")  # Load from .env

def fetch_poster_and_url(movie_id):
    """Fetch multiple poster image URLs + movie page link."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={API_KEY}"
    data = requests.get(url).json()

    posters = data.get('posters', [])
    
    if posters:
        # Construct full URLs for posters
        poster_urls = [
            "https://image.tmdb.org/t/p/w500" + poster['file_path']
            for poster in posters
        ]
    else:
        poster_urls = ["https://via.placeholder.com/500x750?text=No+Poster"]

    # Movie page URL
    movie_url = f"https://www.themoviedb.org/movie/{movie_id}"

    return poster_urls, movie_url

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_links = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url, movie_url = fetch_poster_and_url(movie_id)
        recommended_posters.append(poster_url)
        recommended_links.append(movie_url)
    return recommended_movies, recommended_posters, recommended_links


# Load data
movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load compressed similarity.pkl.gz
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters, links = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <a href="{links[idx]}" target="_blank">
                    <img src="{posters[idx]}" style="width:150px; border-radius:10px; box-shadow:0px 4px 10px rgba(0,0,0,0.5);">
                </a>
                <p style="text-align:center; font-weight:bold;">{names[idx]}</p>
                """,
                unsafe_allow_html=True
            )
