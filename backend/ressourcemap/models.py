from django.db import models

class Map(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    image = models.ImageField()

class RessourceType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    icon = models.ImageField()
    

class RessourceNode(models.Model):
    id = models.IntegerField(primary_key=True)
    x = models.IntegerField()
    y = models.IntegerField()
    ressource_type = models.ForeignKey(RessourceType, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)