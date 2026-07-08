from django.db import models

class Credencial(models.Model):
    OPCIONES_TURNO = [
        ('Día', 'Día'),
        ('Noche', 'Noche'),
        ('Reimpresión de credencial', 'Reimpresión de credencial'),
    ]

    cedula = models.CharField(max_length=10, unique=True, verbose_name="Cédula")
    apellidos_nombres = models.CharField(max_length=150, verbose_name="Apellidos y Nombres")
    turno = models.CharField(max_length=50, choices=OPCIONES_TURNO, verbose_name="Turno")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Credencial"
        verbose_name_plural = "Credenciales"
        ordering = ['fecha_registro']

    def __str__(self):
        return f"{self.cedula} - {self.apellidos_nombres}"