import csv
import pymysql
import json
import ast

# Connexion à la base de données
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="7iJoxvKgMGw4x3nBXMAt",
    db="recsys"
)

try:
    # Create a cursor object
    cursor = connection.cursor()

    # Create a function to insert data into the tables
    def insert_data(table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(data.values()))

    # Open the CSV file and read the data
    with open('data2.csv', 'r') as file:
        csv_data = csv.DictReader(file)

        # Iterate over each row in the CSV file
        for row in csv_data:
            # Insert data into the 'recipes' table
            recipe_data = {
                'id': int(row['id']),
                'name': row['name'],
                'minutes': int(row['minutes']),
                'contributor_id': int(row['contributor_id']),
                'submitted': row['submitted'],
                'description': row['description'],
                'n_steps': int(row['n_steps']),
                'nutrition': row['nutrition']
            }
            insert_data('recipes', recipe_data)

            # Insert data into the 'steps' table
            steps_str = row['steps']
            steps_str = steps_str.replace('[', '').replace(']', '')
            steps_str = steps_str.replace("'", "").replace('"', '')
            steps = [step.strip() for step in steps_str.split(',')]
            for step_number, description in enumerate(steps, start=1):
                step_data = {
                    'recipe_id': int(row['id']),
                    'step_number': step_number,
                    'description': description
                }
                insert_data('steps', step_data)

                # Insert data into the 'recipe_steps' table
                cursor.execute("SELECT id FROM steps WHERE recipe_id=%s AND step_number=%s",
                            (int(row['id']), step_number))
                step_id = cursor.fetchone()
                if step_id is not None:
                    recipe_step_data = {
                        'recipe_id': int(row['id']),
                        'step_id': step_id[0]
                    }
                    insert_data('recipe_steps', recipe_step_data)

            # Insert data into the 'tags' table
            tags_str = row['ingredients']
            tags_str = tags_str.replace('[', '').replace(']', '')
            tags_str = tags_str.replace("'", "").replace('"', '')
            tags = [tag.strip() for tag in tags_str.split(',')]
            for tag_name in tags:
                # Check if the tag already exists in the table
                cursor.execute("SELECT id FROM tags WHERE name=%s", tag_name)
                tag_id = cursor.fetchone()

                if tag_id is None:
                    # Insert a new tag into the 'tags' table
                    cursor.execute("INSERT INTO tags (name) VALUES (%s)", tag_name)
                    tag_id = cursor.lastrowid

                # Insert data into the 'recipe_tags' table
                recipe_tag_data = {
                    'recipe_id': int(row['id']),
                    'tag_id': tag_id
                }
                insert_data('recipe_tags', recipe_tag_data)

            # Insert data into the 'ingredients' table
            ingredients_str = row['ingredients']
            ingredients_str = ingredients_str.replace('[', '').replace(']', '')
            ingredients_str = ingredients_str.replace("'", "").replace('"', '')
            ingredients = [ingredient.strip() for ingredient in ingredients_str.split(',')]
            for ingredient_name in ingredients:
                # Check if the ingredient already exists in the table
                cursor.execute("SELECT id FROM ingredients WHERE name=%s", ingredient_name)
                ingredient_id = cursor.fetchone()

                if ingredient_id is None:
                    # Insert a new ingredient into the 'ingredients' table
                    cursor.execute("INSERT INTO ingredients (name) VALUES (%s)", ingredient_name)
                    ingredient_id = cursor.lastrowid

                # Insert data into the 'recipe_ingredients' table
                recipe_ingredient_data = {
                    'recipe_id': int(row['id']),
                    'ingredient_id': ingredient_id,
                    'quantity': row['n_ingredients']
                }
                insert_data('recipe_ingredients', recipe_ingredient_data)

    # Commit the changes to the database
    connection.commit()
    print("Data insertion completed successfully!")

except Exception as e:
    # Rollback the changes if an error occurs
    connection.rollback()
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
