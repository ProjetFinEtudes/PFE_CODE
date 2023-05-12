import pymysql
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Load the Spacy language model

nlp = spacy.load("en_core_web_sm")

# Establish a connection to the database
connection = pymysql.connect(
    host='10.5.0.2',
    port=3306,
    user='root',
    password='7iJoxvKgMGw4x3nBXMAt',
    database='recsys',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
    # Retrieve recipe names and ingredient lists from the database
query = """
SELECT r.name, GROUP_CONCAT(i.name ORDER BY i.name SEPARATOR ',') AS ingredient_list
FROM recipes AS r
INNER JOIN recipe_ingredients AS ri ON r.id = ri.recipe_id
INNER JOIN ingredients AS i ON ri.ingredient_id = i.id
GROUP BY r.name
"""
with connection.cursor() as cursor:
    query1 = "SELECT name FROM ingredients"
    cursor.execute(query1)
    ingredient_words = [name['name'] for name in cursor.fetchall()]
    cursor.execute(query)
    result = cursor.fetchall()
# Function to extract ingredients from user input text
def extract_ingredients(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    ingredients = []

    for token in doc:
        if token.pos_ == "NOUN" and token.text.lower() in ingredient_words:
            ingredients.append(token.text)

    return ingredients
def recommend_recipes(ingredients):


    # Create ingredient list for each recipe
    recipes = []
    for row in result:
        recipe_name = row['name']
        ingredient_list = row['ingredient_list']
        recipes.append(ingredient_list)
    #print(ingredients)
    print(recipes)
    # Transform ingredient lists into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(recipes)

    # Transform the input ingredients into a TF-IDF vector
    input_vector = vectorizer.transform([','.join(ingredients)])

    # Compute cosine similarity between input vector and recipe vectors
    similarities = cosine_similarity(tfidf_matrix, input_vector)

    # Sort recipes based on similarity scores
    sorted_indices = np.argsort(similarities, axis=0)[::-1].flatten()
    sorted_recipes = [result[i] for i in sorted_indices]

    return (sorted_recipes[:5],sorted_indices)
# Example usage
text_input = "'beef broth,butter,flour,fresh dill,juice of lemon"
ingredients_list = extract_ingredients(text_input)
# Close the database connection
connection.close()

