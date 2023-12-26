from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

class Blog(models.Model):
    name = models.CharField(max_length=255)
    tagline = models.TextField()
    
    def __str__(self):
        return self.name
    

class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique= True)
    
    def __str__(self):
        return self.name

class Entry(models.Model):
    blog= models.ForeignKey("Blog", on_delete=models.CASCADE)
    headline= models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField('date published', auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    authors = models.ManyToManyField(to=Author)
    number_of_comments = models.IntegerField(default= 0)
    rating= models.IntegerField(default= 0, validators= [MaxValueValidator(10, message="Rating cannot be above 10"), MinValueValidator(0, message="Rating cannot be below 0")])
    
    class Meta:
        ordering = ["pub_date"]
