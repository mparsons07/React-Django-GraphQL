from django.db import models

# Create your models here.
# Build a new database model
class Track(models.Model):
    # auto id field
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

