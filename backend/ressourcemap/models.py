from django.db import models

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

class Ressource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    icon = models.ImageField()
    image = models.ImageField(null=True,  blank=True)
    description = models.TextField()
    obtained_from = models.TextField(null=True,  blank=True)
    stack_size = models.IntegerField()
    ressource_category = models.ForeignKey(RessourceCategory, on_delete=models.CASCADE, related_name="ressources")

    def __str__(self):
        return self.name
    
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
    processing_time = models.PositiveIntegerField()  # Processing time in seconds or minutes
    crafting_station = models.ForeignKey(CraftingStation, on_delete=models.CASCADE, null=True,  blank=True)
    ingredients = models.ManyToManyField(Ressource, through='RecipeIngredient', related_name="used_in")
    amount_crafted = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    resource = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.resource.name} in {self.recipe.name}"