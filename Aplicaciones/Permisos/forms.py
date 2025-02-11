from django import forms
from .models import Municipio, Condicion

# VALIDACIÓN PERSONALIZADA PARA ZONAS
def validar_zonas(value):
    if value < 3 or value > 100:
        raise forms.ValidationError("El número de zonas debe estar entre 3 y 100.")

class MunicipioForm(forms.ModelForm):
    zonas = forms.IntegerField(
        validators=[validar_zonas],
        widget=forms.NumberInput(attrs={'min': '3', 'max': '100', 'placeholder': 'Ingrese un número entre 3 y 100'})
    )

    class Meta:
        model = Municipio
        fields = ['nombre', 'zonas']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del municipio'}),
        }

class CondicionForm(forms.ModelForm):
    class Meta:
        model = Condicion
        fields = ['municipio', 'tipo_construccion', 'area_verde', 'servicios_basicos', 'facil_acceso']
        widgets = {
            'municipio': forms.Select(),
            'tipo_construccion': forms.Select(),
            'area_verde': forms.CheckboxInput(),
            'servicios_basicos': forms.CheckboxInput(),
            'facil_acceso': forms.CheckboxInput(),
        }

from django import forms
from django.core.validators import RegexValidator, EmailValidator
from .models import Proyecto, Autorizacion

# 🔹 Validación personalizada para el nombre del proyecto (sin caracteres especiales)
nombre_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9\s ]+$',
    message="El nombre solo puede contener letras y números."
)

# 🔹 Validación personalizada para nombres de personas (solo letras)
responsable_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]+$',
    message="El nombre solo puede contener letras."
)

# 🔹 Validación de email
email_validator = EmailValidator(message="Debe ser un email válido.")

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'municipio', 'tipo_proyecto', 'area_verde', 'servicios_basicos', 'facil_acceso', 'responsable', 'email','plano']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del proyecto'}),
            'descripcion': forms.Textarea(attrs={'placeholder': 'Ingrese la descripción', 'rows': 4}),
            'municipio': forms.Select(),
            'tipo_proyecto': forms.Select(),
            'area_verde': forms.CheckboxInput(),
            'servicios_basicos': forms.CheckboxInput(),
            'facil_acceso': forms.CheckboxInput(),
            'responsable': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del responsable'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese el email'}),
            'plano': forms.ClearableFileInput(attrs={'class': 'file', 'data-show-upload': 'true', 'data-show-caption': 'true'}),
        }
    
    # 📌 Validaciones personalizadas
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not nombre.replace(" ", "").isalnum():
            raise forms.ValidationError("El nombre solo puede contener letras, números y espacios.")
        return nombre


    def clean_responsable(self):
        responsable = self.cleaned_data['responsable']
        if not responsable.replace(" ", "").isalpha():
            raise forms.ValidationError("El nombre solo puede contener letras.")
        return responsable


class AutorizacionForm(forms.ModelForm):
    class Meta:
        model = Autorizacion
        fields = ['proyecto', 'responsable', 'email']  # 🔹 Se elimina el campo 'autorizacion' para que no aparezca en el formulario de creación
        widgets = {
            'proyecto': forms.Select(),
            'responsable': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del responsable'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese el email'}),
        }

    # 📌 Validar que solo se pueda aprobar si el proyecto cumple los requisitos
    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:  # Solo validar si estamos editando
            proyecto = self.instance.proyecto
            condiciones_municipio = Condicion.objects.filter(municipio=proyecto.municipio, tipo_construccion=proyecto.tipo_proyecto)
            
            if condiciones_municipio.exists():
                condicion = condiciones_municipio.first()
                
                if (condicion.area_verde and not proyecto.area_verde) or \
                   (condicion.servicios_basicos and not proyecto.servicios_basicos) or \
                   (condicion.facil_acceso and not proyecto.facil_acceso):
                    if self.instance.autorizacion == "aprobado":
                        raise forms.ValidationError("Este proyecto no cumple con los requisitos obligatorios. No puede ser aprobado.")
        
        return cleaned_data
    def clean_responsable(self):
        responsable = self.cleaned_data['responsable']
        if not responsable.replace(" ", "").isalpha():
            raise forms.ValidationError("El nombre solo puede contener letras.")
        return responsable
