from django.db import models
from django.forms.models import model_to_dict

class Map(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    image = models.ImageField()

    def __str__(self):
        return self.name

class RessourceCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name
    
    def to_json(self):
        # Use Django's model_to_dict to serialize RessourceCategory fields
        category_dict = model_to_dict(self, fields=['id', 'name'])
        # Use the related_name 'ressources' to access all related Ressource objects
        category_dict['ressources'] = [ressource.to_json() for ressource in self.ressources.all()]
        return category_dict

class Ressource(models.Model):
    name = models.CharField(max_length=60)
    icon = models.ImageField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    obtained_from = models.TextField(null=True, blank=True)
    stack_size = models.PositiveIntegerField()
    ressource_category = models.ForeignKey('RessourceCategory', related_name='ressources', on_delete=models.CASCADE, null=True, blank=True)
    used_in = models.ManyToManyField('Recipe', through='RecipeIngredient')
    is_crafted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def to_json(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])
    
class RessourceNode(models.Model):
    id = models.AutoField(primary_key=True)
    x = models.IntegerField()
    y = models.IntegerField()
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE, related_name='ressourcenodes')
    map = models.ForeignKey(Map, on_delete=models.CASCADE, related_name='ressourcenodes')

class CraftingStation(models.Model):
    name = models.CharField(max_length=60)
    # Add any other fields you need for crafting stations

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=60)
    processing_time = models.PositiveIntegerField()
    amount_crafted = models.PositiveIntegerField()
    crafting_station = models.ForeignKey(CraftingStation, on_delete=models.CASCADE)
    output_ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE, related_name='output_of_recipe')

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.ingredient.name} in {self.recipe.name}"