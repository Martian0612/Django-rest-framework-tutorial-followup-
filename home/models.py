from django.db import models

class Color(models.Model):
    color_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.color_name

# Create your models here.
class Person(models.Model):
    color = models.ForeignKey(Color, on_delete= models.CASCADE, null= True, blank = True, related_name= "color")
    name = models.CharField(max_length = 50)
    age = models.CharField(max_length= 3)
    gender_choices = [('female', 'FEMALE'), ('male','MALE'),('unknown','Unknown')]
    gender = models.CharField(max_length= 15, choices= gender_choices , default= 'unknown')

    def __str__(self):
        return self.name

