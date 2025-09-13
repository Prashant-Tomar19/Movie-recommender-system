import streamlit as st
import pickle
import pandas as pd
import requests
import gzip
import os
from dotenv import load_dotenv

# --- Load API key securely from .env ---
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")


# --- Helper functions ---
def fetch_movie_id(title):
    """Search TMDB by title if movie_id is not available."""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    data = requests.get(url).json()
    if data.get("results"):
        return data["results"][0]["id"]
    return None


def fetch_poster(movie_id, title=None):
    """Fetch poster using TMDB movie_id; fallback to title search."""
    if not movie_id and title:
        movie_id = fetch_movie_id(title)

    if not movie_id:  # If still not found
        return "https://via.placeholder.com/500x750?text=No+Poster"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', None)
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    """Recommend similar movies with poster URLs."""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    poster_links = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].get("movie_id", None)
        title = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_id, title)

        recommended_movies.append(title)
        recommended_posters.append(poster_url)
        poster_links.append(poster_url)

    return recommended_movies, recommended_posters, poster_links


# --- Load Data ---
movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity from compressed file
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)


# --- Streamlit UI ---
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
            st.markdown(f"**{names[idx]}**")
            st.image(posters[idx], use_container_width=True)
            st.markdown(f"[🔗 Poster Link]({links[idx]})")  # clickable poster link
