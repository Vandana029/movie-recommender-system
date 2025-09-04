import streamlit as st
import pickle 
import pandas as pd
import requests
import gzip

def fetch_poster(movie_title):
    response = requests.get(f'http://www.omdbapi.com/?t={movie_title}&apikey=4e52dfbb')
    data = response.json()
    return data['Poster']
    #return f'http://img.omdbapi.com/?t={movie_id}&apikey=4e52dfbb'


def recommend(movie_title):
    # Find the index of the selected movie
    movie_index = movies_df[movies_df['title'] == movie_title].index[0]
    # Get the list of similar movies
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    st.write('Top 5 recommended movies:')
    for i in movie_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movies_df.iloc[i[0]].title))  
    return recommended_movies, recommended_movies_posters



movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies_df = pd.DataFrame(movies_dict)
#similarity = pickle.load(open('similarity.pkl','rb'))
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)


st.title('Movie Recommender System')
selector_movie_name = st.selectbox(
    'Select a movie you like:',
    movies_df['title'].values
    )

if st.button('Recommend'):
    names, posters = recommend(selector_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])    
    st.balloons()
    st.snow()
    st.success('Enjoy your movies!')
