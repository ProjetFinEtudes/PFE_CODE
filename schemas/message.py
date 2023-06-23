from pydantic import BaseModel

class Message(BaseModel):
    message: str

class IngredientBase(BaseModel):
    name: str

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    name: str
    minutes: int
    contributor_id: int
    submitted: str
    description: str
    n_steps: int
    nutrition: str

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int

    class Config:
        orm_mode = True

class StepBase(BaseModel):
    recipe_id: int
    step_number: int
    description: str

class StepCreate(StepBase):
    pass

class Step(StepBase):
    id: int

    class Config:
        orm_mode = True

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True

class RecipeIngredientBase(BaseModel):
    recipe_id: int
    ingredient_id: int
    quantity: str

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredient(RecipeIngredientBase):
    class Config:
        orm_mode = True

class RecipeStepBase(BaseModel):
    recipe_id: int
    step_id: int

class RecipeStepCreate(RecipeStepBase):
    pass

class RecipeStep(RecipeStepBase):
    class Config:
        orm_mode = True

class RecipeTagBase(BaseModel):
    recipe_id: int
    tag_id: int

class RecipeTagCreate(RecipeTagBase):
    pass

class RecipeTag(RecipeTagBase):
    class Config:
        orm_mode = True