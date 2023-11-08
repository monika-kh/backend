from django.db import models

# Create your models here.

class Technology(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
        
        
class Experience(models.Model):
    exp = models.DecimalField(max_digits=50, decimal_places=1)
    
    def __str__(self):
        return (str(self.exp))