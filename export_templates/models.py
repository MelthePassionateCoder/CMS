from django.db import models
from advisory.models import Advisory

class ExportTemplate(models.Model):
    advisory = models.ForeignKey(Advisory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.advisory.section}"