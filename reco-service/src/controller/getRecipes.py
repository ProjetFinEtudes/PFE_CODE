import pymysql
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the Spacy language model
nlp = spacy.load("en_core_web_sm")

# Establish a connection to the database


# Function to extract ingredients from user input text
def extract_ingredients(sentence,ingredient_words):
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

def recommend_recipes(user_id, sentence):
    connection = pymysql.connect(
    host='10.5.0.2',
    port=3306,
    user='root',
    password='7iJoxvKgMGw4x3nBXMAt',
    database='recsys',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        # Retrieve recipe names, ingredient lists, tags, and user tags from the database
        query = """
        SELECT r.name, GROUP_CONCAT(i.name ORDER BY i.name SEPARATOR ',') AS ingredient_list, GROUP_CONCAT(t.name ORDER BY t.name SEPARATOR ',') AS tag_list
        FROM recipes AS r
        INNER JOIN recipe_ingredients AS ri ON r.id = ri.recipe_id
        INNER JOIN ingredients AS i ON ri.ingredient_id = i.id
        INNER JOIN recipe_tags AS rt ON r.id = rt.recipe_id
        INNER JOIN tags AS t ON rt.tag_id = t.id
        GROUP BY r.name
        """
        query1 = "SELECT name FROM ingredients"
        cursor.execute(query1)
        ingredient_words = [name['name'] for name in cursor.fetchall()]
        cursor.execute(query)
        result = cursor.fetchall()

        # Retrieve user's food preferences from user_tags
        user_query = """
        SELECT t.name
        FROM user_tags AS ut
        INNER JOIN tags AS t ON ut.id_tag = t.id
        WHERE ut.id_user = %s
        """
        cursor.execute(user_query, user_id)
        user_tags = set(tag['name'] for tag in cursor.fetchall())

    ingredients = extract_ingredients(sentence,ingredient_words)
    # Create ingredient set and tag set for each recipe
    recipes = []
    for row in result:
        recipe_name = row['name']
        ingredient_list = set(row['ingredient_list'].split(','))
        tag_list = set(row['tag_list'].split(','))
        recipes.append((recipe_name, ingredient_list, tag_list))

    # Transform the input ingredients into a set
    input_ingredients = set(ingredients)

    # Calculate Jaccard similarity between input set and recipe sets
    similarities = []
    for recipe in recipes:
        recipe_name, ingredient_list, tag_list = recipe
        similarity = jaccard_similarity(input_ingredients, ingredient_list)
        # Apply additional weight to recipes with matching tags
        if tag_list.intersection(user_tags):
            similarity += 0.1
        similarities.append(similarity)

    # Sort recipes based on similarity scores
    sorted_indices = np.argsort(similarities)[::-1]
    sorted_recipes = [recipes[i][0] for i in sorted_indices]
    connection.close()
    return sorted_recipes[:5]

# Close the database connection
