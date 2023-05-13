import pymysql
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

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
    doc = nlp(sentence)
    ingredients = []

    for token in doc:
        if token.pos_ == "NOUN" and token.text.lower() in ingredient_words:
            ingredients.append(token.text)

    return ingredients

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def recommend_recipes(sentance):
    ingredients = extract_ingredients(sentance)
    # Create ingredient set for each recipe
    recipes = []
    for row in result:
        recipe_name = row['name']
        ingredient_list = set(row['ingredient_list'].split(','))
        recipes.append(ingredient_list)

    # Transform the input ingredients into a set
    input_ingredients = set(ingredients)

    # Calculate Jaccard similarity between input set and recipe sets
    similarities = []
    for recipe in recipes:
        similarity = jaccard_similarity(input_ingredients, recipe)
        similarities.append(similarity)

    # Sort recipes based on similarity scores
    sorted_indices = np.argsort(similarities)[::-1]
    sorted_recipes = [result[i] for i in sorted_indices]

    return sorted_recipes[:5]
# Close the database connection
connection.close()
