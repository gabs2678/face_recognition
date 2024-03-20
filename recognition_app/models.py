from django.db import models

class MissingPerson(models.Model):
    name = models.CharField(max_length=100)
    last_seen = models.DateTimeField()
    image = models.ImageField(upload_to='missing_persons/')

    def __str__(self):
        return self.name