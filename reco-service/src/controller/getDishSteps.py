import pymysql
import re
from difflib import SequenceMatcher
from threading import Lock

# Define a lock to synchronize access to the database connection and cursor
db_lock = Lock()

def get_database_connection():
    conn = pymysql.connect(
        host='10.5.0.2',
        port=3306,
        user='root',
        password='7iJoxvKgMGw4x3nBXMAt',
        database='recsys',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def find_best_match(recipe_names, text):
    best_match = None
    max_ratio = 0
    text = text.lower()

    for name in recipe_names:
        ratio = SequenceMatcher(None, text, name.lower()).ratio()
        if ratio > max_ratio:
            max_ratio = ratio
            best_match = name

    return best_match

def dish_step(text):
    with db_lock:
        # Se connecter à la base de données
        conn = get_database_connection()
        cursor = conn.cursor()

        # Extraire les noms de recettes de la base de données
        query = "SELECT name FROM recipes"
        cursor.execute(query)
        recipe_names = [dish['name'] for dish in cursor.fetchall()]

        # Vérifier s'il y a des recettes dans la base de données
        if not recipe_names:
            cursor.close()
            conn.close()
            return "Aucune recette trouvée dans la base de données."

        # Trouver le nom de recette le plus probable dans le texte
        best_recipe = find_best_match(recipe_names, text)
        if not best_recipe:
            cursor.close()
            conn.close()
            return "No dish found"

        # Requête pour obtenir les étapes de la recette
        query = """
            SELECT s.step_number, s.description
            FROM recipes r
            INNER JOIN recipe_steps rs ON r.id = rs.recipe_id
            INNER JOIN steps s ON rs.step_id = s.id
            WHERE r.name = %s
            ORDER BY s.step_number
        """
        cursor.execute(query, (best_recipe,))
        result = cursor.fetchall()

        # Fermer le curseur et la connexion à la base de données
        cursor.close()
        conn.close()

        # Vérifier s'il y a des étapes pour la recette trouvée
        if len(result) == 0:
            return "No dish found with that name"

        # Générer la liste des étapes à suivre
        steps_list = [f"Step {step['step_number']}: {step['description']}" for step in result]
        return "\n".join(steps_list)
