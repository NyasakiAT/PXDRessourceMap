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
    description = models.TextField()
    ressource_category = models.ForeignKey(RessourceCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class RessourceNode(models.Model):
    id = models.AutoField(primary_key=True)
    x = models.IntegerField()
    y = models.IntegerField()
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE, related_name='ressourcenodes')
    map = models.ForeignKey(Map, on_delete=models.CASCADE, related_name='ressourcenodes')
