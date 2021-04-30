#DJANGO
from django.db import models




class AbstractPruebaModel(models.Model):
    """
        Abstract model for add datetime fields in others models
    """
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(null=True)
    class Meta:
        abstract = True