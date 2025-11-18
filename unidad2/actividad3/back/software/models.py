from django.db import models


class Software(models.Model):
    version = models.CharField(max_length=50)
    tipo = models.CharField(max_length=100)
    fecha_publicacion = models.DateField()
    firewall = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tipo} v{self.version}"

