import streamlit as st
import easyocr
from PIL import Image
from joblib import load
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
import plotly.express as px

reader = easyocr.Reader(["en"])
tfidf_matrix = load(
    "/Users/irenenguyen/Desktop/cosmetic-ingredient/tfidf_matrix.joblib"
)
vectorizer = load("/Users/irenenguyen/Desktop/cosmetic-ingredient/vectorizer.joblib")


@st.cache_data
def load_data(url):
    return pd.read_csv(url)


ingredients = load_data(
    "/Users/irenenguyen/Desktop/cosmetic-ingredient/data/ingredients.csv"
)


def get_matching_ing(user_ingredients):
    user_ingredients = [i.lower() for i in user_ingredients]
    str = " ".join(user_ingredients)
    result = re.split(r"[,:;]", str)
    user_vectors = vectorizer.transform(result)
    similarity_scores = cosine_similarity(user_vectors, tfidf_matrix)
    most_similar_indices = similarity_scores.argmax(axis=1)
    matching_ingredients = ingredients.iloc[most_similar_indices]["Ingredient"].tolist()
    final_ing = list(set(matching_ingredients))
    return final_ing


def get_df(ings):
    return ingredients[ingredients["Ingredient"].isin(ings)]


def calc_proportions(lst):
    total = len(lst)
    groups = [
        ingredients.loc[ingredients["Ingredient"] == i, "Group"].values[0] for i in lst
    ]
    freqs = {}
    for g in groups:
        if g not in freqs:
            freqs[g] = 1
        else:
            freqs[g] += 1
    res_dict = {key: round(value / total, 2) for key, value in freqs.items()}
    res = {"Function": list(res_dict.keys()), "Proportion": list(res_dict.values())}
    final = pd.DataFrame(res).sort_values("Proportion", ascending=False)
    return final


upload_img = st.file_uploader(
    "Upload an image of a product label", type=["jpg", "jpeg", "png"]
)
if upload_img is not None:
    image = Image.open(upload_img)
    st.image(image, caption="Uploaded Label", use_column_width=True)
    results = reader.readtext(image)
    user_ings = [r[1] for r in results]
    matching_ings = get_matching_ing(user_ings)
    props = calc_proportions(matching_ings)
    col1, col2 = st.columns(2)
    col1.write(matching_ings)
    if col2.button("See function break down for each ingredient"):
        st.dataframe(get_df(matching_ings), hide_index=True)
    fig = px.pie(props, values="Proportion", names="Function")
    st.plotly_chart(fig)
