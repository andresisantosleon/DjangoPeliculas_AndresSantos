from django.db import models

# Create your models here.

class Peliculas(models.Model):

    nombre=models.TextField(max_length=50)
    votos=models.IntegerField()
    imdbID=models.TextField(max_length=50, default='')

    @classmethod
    def constructor_1(cls, nombreC, imdbIDC, votosC):
        pelicula=cls(nombre=nombreC, imdbID=imdbIDC, votos=votosC)
        return pelicula
    

    

