from django.db import models

# Dashoard
class Dashboard(models.Model):
    title = models.CharField(max_length=250, default="")
    icon = models.CharField(max_length=250, default="")
    url = models.CharField(max_length=250, default="")

    def __str__(self):
        return str(self.pk) + ' - ' + self.title
