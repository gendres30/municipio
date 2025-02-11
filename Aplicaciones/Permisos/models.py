from django.db import models

class Municipio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    zonas = models.IntegerField()  # Número entero entre 3 y 100

    def __str__(self):
        return self.nombre

class Condicion(models.Model):
    TIPO_CONSTRUCCION_CHOICES = [
        ("casa_pequena_1p", "Casa pequeña de una planta"),
        ("casa_mediana_1p", "Casa mediana de una planta"),
        ("casa_grande_1p", "Casa grande de una planta"),
        ("casa_pequena_2p", "Casa pequeña de 2 plantas"),
        ("casa_mediana_2p", "Casa mediana de 2 plantas"),
        ("casa_grande_2p", "Casa grande de 2 plantas"),
        ("casa_3p", "Casa de 3 plantas"),
        ("casa_mas_3p", "Casa de +3 plantas"),
        ("local_pequeno_1p", "Local pequeño de 1 planta"),
        ("local_mediano_1p", "Local mediano de 1 planta"),
        ("local_grande_1p", "Local grande de 1 planta"),
        ("local_mediano_2p", "Local mediano de 2 plantas"),
        ("local_grande_2p", "Local grande de 2 plantas"),
        ("local_3p", "Local de 3 plantas"),
        ("local_mas_3p", "Local de +3 plantas"),
        ("zona_recreativa", "Zona recreativa"),
        ("centro_comercial", "Centro comercial"),
        ("gasolinera", "Gasolinera"),
        ("condominio", "Condominio"),
        ("edificio_estado", "Edificio del estado"),
        ("espacios_salud", "Espacios de salud"),
    ]

    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name="condiciones")
    tipo_construccion = models.CharField(max_length=50, choices=TIPO_CONSTRUCCION_CHOICES)
    area_verde = models.BooleanField(default=False)
    servicios_basicos = models.BooleanField(default=False)
    facil_acceso = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_tipo_construccion_display()} - {self.municipio.nombre}"


from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Proyecto(models.Model):
    ESTADO_PROYECTO = [
        ("ingresado", "Ingresado"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
    ]

    TIPO_PROYECTO_CHOICES = [
        ("casa_pequena_1p", "Casa pequeña de una planta"),
        ("casa_mediana_1p", "Casa mediana de una planta"),
        ("casa_grande_1p", "Casa grande de una planta"),
        ("casa_pequena_2p", "Casa pequeña de 2 plantas"),
        ("casa_mediana_2p", "Casa mediana de 2 plantas"),
        ("casa_grande_2p", "Casa grande de 2 plantas"),
        ("casa_3p", "Casa de 3 plantas"),
        ("casa_mas_3p", "Casa de +3 plantas"),
        ("local_pequeno_1p", "Local pequeño de 1 planta"),
        ("local_mediano_1p", "Local mediano de 1 planta"),
        ("local_grande_1p", "Local grande de 1 planta"),
        ("local_mediano_2p", "Local mediano de 2 plantas"),
        ("local_grande_2p", "Local grande de 2 plantas"),
        ("local_3p", "Local de 3 plantas"),
        ("local_mas_3p", "Local de +3 plantas"),
        ("zona_recreativa", "Zona recreativa"),
        ("centro_comercial", "Centro comercial"),
        ("gasolinera", "Gasolinera"),
        ("condominio", "Condominio"),
        ("edificio_estado", "Edificio del estado"),
        ("espacios_salud", "Espacios de salud"),
    ]

    nombre = models.CharField(
        max_length=100, 
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9\s]+$', message="Solo se permiten letras y números.")]
    )
    descripcion = models.TextField(max_length=1000)
    municipio = models.ForeignKey("Municipio", on_delete=models.CASCADE)
    tipo_proyecto = models.CharField(max_length=50, choices=TIPO_PROYECTO_CHOICES)
    area_verde = models.BooleanField(default=False)
    servicios_basicos = models.BooleanField(default=False)
    facil_acceso = models.BooleanField(default=False)
    estado = models.CharField(max_length=10, choices=ESTADO_PROYECTO, default="ingresado")
    responsable = models.CharField(
        max_length=100, 
        validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$', message="Solo se permiten letras.")]
    )
    email = models.EmailField(validators=[EmailValidator(message="Debe ser un email válido.")])
    plano = models.ImageField(upload_to='planos', null=True, blank=True)  # 🖼️ Nuevo campo para subir imágenes
    def __str__(self):
        return self.nombre

class Autorizacion(models.Model):
    AUTORIZACION_ESTADOS = [
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
    ]

    proyecto = models.OneToOneField(Proyecto, on_delete=models.CASCADE)
    responsable = models.CharField(
        max_length=100, 
        validators=[RegexValidator(regex=r'^[a-zA-Z\s]+$', message="Solo se permiten letras.")]
    )
    email = models.EmailField(validators=[EmailValidator(message="Debe ser un email válido.")])
    autorizacion = models.CharField(max_length=10, choices=AUTORIZACION_ESTADOS)

    def __str__(self):
        return f"Autorización para {self.proyecto.nombre} - {self.autorizacion}"

# 📌 ACTUALIZAR ESTADO DEL PROYECTO CUANDO SE CREA UNA AUTORIZACIÓN
@receiver(post_save, sender=Autorizacion)
def actualizar_estado_proyecto(sender, instance, **kwargs):
    instance.proyecto.estado = instance.autorizacion  # Cambia el estado según la autorización
    instance.proyecto.save()
