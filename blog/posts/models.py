from django.db import models

# Create your models here.
class Images(models.Model):
    file = models.FileField(blank = True, upload_to='images/')