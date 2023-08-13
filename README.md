# cosmetic-ingredient

Link to the app on Streamlit Cloud: [](https://cosmetic-ingredient.streamlit.app/)
A multi-page Streamlit web app with 2 main pages:

**1. Ingredients reader & function analyzer:**
- read cosmetic ingredients from the photo of a product label
- match these ingredients against the dataset that I created by scraping the largest database to date of cosmetic ingredients (more info below)
- calculate and show a visualization of the breakdown of the cosmetic product's main functions (e.g. 

The photos below shows an example analysis on 2 different products, the 1st being a serum and the 2nd one a cleanser:
<img width="780" alt="Screenshot 2023-08-13 at 12 00 25" src="https://github.com/irenehng/cosmetic-ingredient/assets/113161586/52327e9f-8b9a-41c5-a795-f2c2328c4cd4" height="650px" width="3px">
<img width="939" alt="Screenshot 2023-08-13 at 14 23 42" src="https://github.com/irenehng/cosmetic-ingredient/assets/113161586/1232a3b1-d6c7-41ed-8390-4e9991dce5f2" height = "650px">

**2. Recommender:**
- read cosmetic ingredients from the photo of a product label
- utilize a similarity-based recommender model to recommend products with similar ingredient profiles to the user's favorite product
- only show results that are suitable to the user's skintype

Example usage in the photo below. The input photo was a serum by Estee Lauder, and the model recommended some Estee Lauder products in the same line:

<img width="808" alt="Screenshot 2023-08-13 at 14 56 16" src="https://github.com/irenehng/cosmetic-ingredient/assets/113161586/d327d994-36c2-42f4-815b-da4670ac473e" height="650px">
