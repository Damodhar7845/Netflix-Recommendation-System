import streamlit as st
import pandas as pd
import pickle

# ==================================
# Page Config
# ==================================

st.set_page_config(
    page_title="Netflix Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ==================================
# Load Saved Files
# ==================================

movie_info = pickle.load(open("movie_info.pkl", "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))
movie_titles = pickle.load(open("movie_titles.pkl", "rb"))

# ==================================
# Recommendation Function
# ==================================

def recommend(movie_name):

    if movie_name not in movie_titles:
        return None

    idx = movie_titles.index(movie_name)

    distances = similarity_scores[idx]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for movie in movies_list:

        title = movie_titles[movie[0]]

        movie_row = movie_info[movie_info['Title'] == title]

        if len(movie_row) > 0:

            avg_rating = movie_row['avg_rating'].values[0]
            num_ratings = movie_row['num_ratings'].values[0]

            recommended_movies.append([
                title,
                round(avg_rating, 2),
                int(num_ratings)
            ])

    return pd.DataFrame(
        recommended_movies,
        columns=[
            "Movie",
            "Avg Rating",
            "Number of Ratings"
        ]
    )

# ==================================
# Header
# ==================================

st.title("🎬 Netflix Movie Recommendation System")

st.markdown(
    """
    Get personalized movie recommendations using **Collaborative Filtering**.
    """
)

# ==================================
# Statistics
# ==================================

st.write("### Dataset Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Movies", len(movie_titles))

with col2:
    st.metric("Users", "368,751")

with col3:
    st.metric("Ratings Dataset", "22M+")

st.markdown("---")

# ==================================
# Movie Selection
# ==================================

selected_movie = st.selectbox(
    "Select a Movie",
    sorted(movie_titles)
)

# ==================================
# Recommendation Button
# ==================================

if st.button("🎯 Recommend Movies"):

    result = recommend(selected_movie)

    if result is None:

        st.error("Movie not found in dataset.")

    else:

        st.success(
            f"Top 5 recommendations for '{selected_movie}'"
        )

        st.dataframe(
            result,
            use_container_width=True
        )

# ==================================
# Footer
# ==================================

st.markdown("---")

st.caption(
    "Developed by Reena Jasper Bulla | Netflix Movie Recommendation System"
)