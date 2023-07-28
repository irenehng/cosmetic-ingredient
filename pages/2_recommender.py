import streamlit as st
import pandas as pd
import easyocr
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from joblib import load
import re

reader = easyocr.Reader(["en"])


@st.cache_data
def load_jl(f):
    return load(f)


@st.cache_data
def load_df(url):
    return pd.read_csv(url)


input_vectorizer = load_jl(
    "/Users/irenenguyen/Desktop/cosmetic-ingredient/vectorizer.joblib"
)
prod_vectorizer = load_jl(
    "/Users/irenenguyen/Desktop/cosmetic-ingredient/rec_vectorizer.joblib"
)
prod_matrix = load_jl("rec_matrix.joblib")
prods = load_df("/Users/irenenguyen/Desktop/cosmetic-ingredient/data/cosmetics.csv")
ingredients = load_df(
    "/Users/irenenguyen/Desktop/cosmetic-ingredient/data/ingredients.csv"
)
tfidf_matrix = load_jl(
    "/Users/irenenguyen/Desktop/cosmetic-ingredient/tfidf_matrix.joblib"
)


def get_matching_ing(image):
    results = reader.readtext(image)
    user_ingredients = [r[1] for r in results]
    user_ingredients = [i.lower() for i in user_ingredients]
    str = " ".join(user_ingredients)
    result = re.split(r"[,:;]", str)
    user_vectors = input_vectorizer.transform(result)
    similarity_scores = cosine_similarity(user_vectors, tfidf_matrix)
    most_similar_indices = similarity_scores.argmax(axis=1)
    matching_ingredients = ingredients.iloc[most_similar_indices]["Ingredient"].tolist()
    final_ing = list(set(matching_ingredients))
    return final_ing


def get_recs(target, n=5):
    similarity_matrix = cosine_similarity(prod_matrix)
    target_processed = " ".join(sorted(target))
    target_vector = prod_vectorizer.transform([target_processed])
    similarities = cosine_similarity(target_vector, prod_matrix)[0]
    indices = similarities.argsort()[::-1]
    general_recs = prods.iloc[indices]
    global skin_type
    if skin_type is not None:
        recs = general_recs[general_recs[skin_type] == 1]
        if recs is not None:
            general_recs = recs
    return general_recs[["Label", "Brand", "Name", "Price", "Rank"]].head(n)


st.header(
    "Get product recommendations based on the ingredient list of your favorite product!"
)
skin_type = st.radio(
    "Pick your skin type", ["Combination", "Dry", "Oily", "Normal", "Sensitive"]
)
upload_img = st.file_uploader(
    "Upload an image of a product label", type=["jpg", "jpeg", "png"]
)
if upload_img is not None:
    image = Image.open(upload_img)
    st.header("Product Recs For You:")
    matching_ings = get_matching_ing(image)
    recs = get_recs(matching_ings)
    st.dataframe(recs)
