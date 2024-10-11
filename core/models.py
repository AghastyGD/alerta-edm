from django.db import models
from autoslug import AutoSlugField

class PowerOutage(models.Model):
    area = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    affected_zone = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slug = AutoSlugField(populate_from='state', unique=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.area} - {self.state}"
    
