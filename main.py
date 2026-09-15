import streamlit as st
import pickle
import pandas as pd
import requests


st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


st.markdown("""
<style>

.main {
    background-color: #0f0f0f;
}

h1 {
    text-align: center;
    font-size: 50px;
}

.movie-title {
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)



def fetch_poster(movie_id):
  api_key = st.secrets["TMDB_API_KEY"]
  resposnse = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-us')
  data = resposnse.json()
  return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

def recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)),reverse = True, key = lambda x: x[1])[1:6]

  recommend_movies = []
  recommend_movies_poster = []

  for i in movies_list:

    movie_id = movies.iloc[i[0]].movie_id
    recommend_movies.append(movies.iloc[i[0]].title)

    recommend_movies_poster.append(fetch_poster(movie_id))
  return recommend_movies, recommend_movies_poster

similarity = pickle.load(open('model/similarity.pkl','rb'))
movies_dict = pickle.load(open('model/movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
st.title('Movie Recommender System')

selected_movie = st.selectbox('Select Your Movie:',movies['title'].values)

if st.button('Recommend'):
  names, posters = recommend(selected_movie)   
  cols = st.columns(5)

  for i in range(5):
      with cols[i]:
          st.text(names[i])
          st.image(posters[i])