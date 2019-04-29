from django.db import models

class Upload(models.Model):

    file = models.FileField()
