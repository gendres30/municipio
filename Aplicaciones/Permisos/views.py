from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Municipio, Condicion
from .forms import MunicipioForm, CondicionForm

# 📌 LISTAR MUNICIPIOS
def listar_municipios(request):
    municipios = Municipio.objects.all()
    return render(request, 'municipios/listar.html', {'municipios': municipios})

# 📌 CREAR MUNICIPIO
def crear_municipio(request):
    if request.method == "POST":
        form = MunicipioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Municipio creado con éxito.")
            return redirect('listar_municipios')
        else:
            messages.error(request, "Error al crear el municipio. Revise los datos.")
    else:
        form = MunicipioForm()
    
    return render(request, 'municipios/formulario.html', {'form': form, 'titulo': "Crear Municipio"})

# 📌 EDITAR MUNICIPIO
def editar_municipio(request, pk):
    municipio = get_object_or_404(Municipio, pk=pk)
    
    if request.method == "POST":
        form = MunicipioForm(request.POST, instance=municipio)
        if form.is_valid():
            form.save()
            messages.success(request, "Municipio actualizado con éxito.")
            return redirect('listar_municipios')
        else:
            messages.error(request, "Error al actualizar el municipio. Revise los datos.")
    else:
        form = MunicipioForm(instance=municipio)

    return render(request, 'municipios/formulario.html', {'form': form, 'titulo': "Editar Municipio"})

# 📌 ELIMINAR MUNICIPIO
def eliminar_municipio(request, pk):
    municipio = get_object_or_404(Municipio, pk=pk)
    
    if request.method == "POST":
        municipio.delete()
        messages.success(request, "Municipio eliminado con éxito.")
        return redirect('listar_municipios')
    
    return render(request, 'municipios/eliminar.html', {'municipio': municipio})

# 📌 LISTAR CONDICIONES
def listar_condiciones(request):
    condiciones = Condicion.objects.all()
    return render(request, 'condiciones/listar.html', {'condiciones': condiciones})

# 📌 CREAR CONDICIÓN
def crear_condicion(request):
    if request.method == "POST":
        form = CondicionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Condición creada con éxito.")
            return redirect('listar_condiciones')
        else:
            messages.error(request, "Error al crear la condición. Revise los datos.")
    else:
        form = CondicionForm()
    
    return render(request, 'condiciones/formulario.html', {'form': form, 'titulo': "Crear Condición"})

# 📌 EDITAR CONDICIÓN
def editar_condicion(request, pk):
    condicion = get_object_or_404(Condicion, pk=pk)
    
    if request.method == "POST":
        form = CondicionForm(request.POST, instance=condicion)
        if form.is_valid():
            form.save()
            messages.success(request, "Condición actualizada con éxito.")
            return redirect('listar_condiciones')
        else:
            messages.error(request, "Error al actualizar la condición. Revise los datos.")
    else:
        form = CondicionForm(instance=condicion)

    return render(request, 'condiciones/formulario.html', {'form': form, 'titulo': "Editar Condición"})

# 📌 ELIMINAR CONDICIÓN
def eliminar_condicion(request, pk):
    condicion = get_object_or_404(Condicion, pk=pk)
    
    if request.method == "POST":
        condicion.delete()
        messages.success(request, "Condición eliminada con éxito.")
        return redirect('listar_condiciones')
    
    return render(request, 'condiciones/eliminar.html', {'condicion': condicion})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Proyecto, Autorizacion, Condicion
from .forms import ProyectoForm, AutorizacionForm

# 📌 LISTAR PROYECTOS
def listar_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos/listar.html', {'proyectos': proyectos})

# 📌 CREAR PROYECTO
from django.core.mail import send_mail

def crear_proyecto(request):
    if request.method == "POST":
        form = ProyectoForm(request.POST, request.FILES)  # 📂 Soporta archivos
        if form.is_valid():
            proyecto = form.save()
            
            # 📧 Enviar email de confirmación
            asunto = "Registro de Proyecto Exitoso"
            mensaje = f"Hola {proyecto.responsable},\n\nTu proyecto '{proyecto.nombre}' ha sido registrado exitosamente en el sistema.\n\nEstado actual: {proyecto.get_estado_display()}\n\nTe notificaremos cuando se revise la autorización."
            send_mail(asunto, mensaje, 'tu_correo@gmail.com', [proyecto.email])

            messages.success(request, "Proyecto creado y correo enviado.")
            return redirect('listar_proyectos')
        else:
            messages.error(request, "Error al crear el proyecto. Revise los datos.")
    else:
        form = ProyectoForm()
    
    return render(request, 'proyectos/formulario.html', {'form': form, 'titulo': "Crear Proyecto"})


# 📌 EDITAR PROYECTO
def editar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    
    if request.method == "POST":
        form = ProyectoForm(request.POST,request.FILES, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, "Proyecto actualizado con éxito.")
            return redirect('listar_proyectos')
        else:
            messages.error(request, "Error al actualizar el proyecto. Revise los datos.")
    else:
        form = ProyectoForm(instance=proyecto)

    return render(request, 'proyectos/formulario.html', {'form': form, 'titulo': "Editar Proyecto"})

# 📌 ELIMINAR PROYECTO
def eliminar_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    
    if request.method == "POST":
        proyecto.delete()
        messages.success(request, "Proyecto eliminado con éxito.")
        return redirect('listar_proyectos')
    
    return render(request, 'proyectos/eliminar.html', {'proyecto': proyecto})

# 📌 LISTAR AUTORIZACIONES
def listar_autorizaciones(request):
    autorizaciones = Autorizacion.objects.all()
    return render(request, 'autorizaciones/listar.html', {'autorizaciones': autorizaciones})

# 📌 CREAR AUTORIZACIÓN (VALIDANDO CONDICIONES DEL MUNICIPIO)
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Autorizacion, Condicion
from .forms import AutorizacionForm

def crear_autorizacion(request):
    if request.method == "POST":
        form = AutorizacionForm(request.POST)
        if form.is_valid():
            autorizacion = form.save(commit=False)
            proyecto = autorizacion.proyecto

            # 🚀 Evaluamos si el proyecto cumple con las condiciones del municipio
            condiciones_municipio = Condicion.objects.filter(municipio=proyecto.municipio, tipo_construccion=proyecto.tipo_proyecto)

            if condiciones_municipio.exists():
                condicion = condiciones_municipio.first()
                
                if (condicion.area_verde and not proyecto.area_verde) or \
                   (condicion.servicios_basicos and not proyecto.servicios_basicos) or \
                   (condicion.facil_acceso and not proyecto.facil_acceso):
                    autorizacion.autorizacion = "rechazado"
                    estado = "RECHAZADO"
                    mensaje_estado = "El proyecto no cumple con los requisitos y ha sido rechazado automáticamente."
                else:
                    autorizacion.autorizacion = "aprobado"
                    estado = "APROBADO"
                    mensaje_estado = "El proyecto cumple con los requisitos y ha sido aprobado automáticamente."

                # 📧 Enviar notificación por correo electrónico
                asunto = f"Actualización de tu Proyecto: {proyecto.nombre}"
                mensaje = f"""
                Hola {proyecto.responsable},

                Tu proyecto '{proyecto.nombre}' ha sido {estado}.

                Estado actual: {estado}.
                {mensaje_estado}

                Gracias por usar nuestro sistema.
                """
                send_mail(asunto, mensaje, 'tu_correo@gmail.com', [proyecto.email])

            autorizacion.save()
            messages.success(request, mensaje_estado)
            return redirect('listar_autorizaciones')
        else:
            messages.error(request, "Error al crear la autorización. Revise los datos.")
    else:
        form = AutorizacionForm()
    
    return render(request, 'autorizaciones/formulario.html', {'form': form, 'titulo': "Crear Autorización"})

# 📌 EDITAR AUTORIZACIÓN
def editar_autorizacion(request, pk):
    autorizacion = get_object_or_404(Autorizacion, pk=pk)

    if request.method == "POST":
        form = AutorizacionForm(request.POST, instance=autorizacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Autorización actualizada con éxito.")
            return redirect('listar_autorizaciones')
        else:
            messages.error(request, "No se puede aprobar este proyecto porque no cumple con las condiciones.")
    else:
        form = AutorizacionForm(instance=autorizacion)

    return render(request, 'autorizaciones/formulario.html', {'form': form, 'titulo': "Editar Autorización"})

# 📌 ELIMINAR AUTORIZACIÓN
def eliminar_autorizacion(request, pk):
    autorizacion = get_object_or_404(Autorizacion, pk=pk)
    
    if request.method == "POST":
        autorizacion.delete()
        messages.success(request, "Autorización eliminada con éxito.")
        return redirect('listar_autorizaciones')
    
    return render(request, 'autorizaciones/eliminar.html', {'autorizacion': autorizacion})



from django.shortcuts import render
from django.http import JsonResponse
from .models import Proyecto, Municipio, Condicion, Autorizacion

# Vista para renderizar la página de inicio
def inicio(request):
    contexto = {
        "total_proyectos": Proyecto.objects.count(),
        "total_municipios": Municipio.objects.count(),
        "total_condiciones": Condicion.objects.count(),
        "total_autorizaciones": Autorizacion.objects.count(),
    }
    return render(request, "inicio.html", contexto)

# API para actualizar estadísticas en tiempo real
def api_estadisticas(request):
    data = {
        "total_proyectos": Proyecto.objects.count(),
        "total_municipios": Municipio.objects.count(),
        "total_condiciones": Condicion.objects.count(),
        "total_autorizaciones": Autorizacion.objects.count(),
    }
    return JsonResponse(data)