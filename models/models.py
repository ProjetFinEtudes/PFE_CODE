from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Auth(Base):
    __tablename__ = 'auth'

    uid = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(Text, nullable=False)


class User(Base):
    __tablename__ = 'user'

    uid = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    genre = Column(String(1), nullable=False)
    auth = relationship("Auth", backref="user", cascade="all, delete")


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    minutes = Column(Integer)
    contributor_id = Column(Integer)
    submitted = Column(Date)
    description = Column(Text)
    n_steps = Column(Integer)
    nutrition = Column(String(255))


class Step(Base):
    __tablename__ = 'steps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    step_number = Column(Integer, nullable=False)
    description = Column(Text)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'

    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)
    quantity = Column(String(255))


class RecipeStep(Base):
    __tablename__ = 'recipe_steps'

    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    step_id = Column(Integer, ForeignKey('steps.id'), primary_key=True)


class RecipeTag(Base):
    __tablename__ = 'recipe_tags'

    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
