from django.db import models

class File(models.Model):
    file = models.ImageField(upload_to="files/")
    
    def __str__(self):
        return self.file.name