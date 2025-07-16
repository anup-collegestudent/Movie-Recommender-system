import pickle
import streamlit as st
import requests


# Function to fetch movie poster from TMDb
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None


# Recommendation function based on movie similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Streamlit UI
st.header('Movie Recommender System')

# Load movie data and similarity matrix (use 'rb' for reading pickle files)
movies = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# List of movie titles for dropdown
movie_list = movies['title'].values

# Dropdown for movie selection
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Button to trigger recommendation
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create columns for displaying recommendations
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.text(recommended_movie_names[idx])
        if recommended_movie_posters[idx]:  # Check if poster is available
            col.image(recommended_movie_posters[idx])
        else:
            col.text("Poster not available")
