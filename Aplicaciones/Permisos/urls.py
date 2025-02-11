from django.urls import path
from . import views

urlpatterns = [
    # 📌 MUNICIPIOS
    path('municipios/', views.listar_municipios, name='listar_municipios'),
    path('municipios/crear/', views.crear_municipio, name='crear_municipio'),
    path('municipios/editar/<int:pk>/', views.editar_municipio, name='editar_municipio'),
    path('municipios/eliminar/<int:pk>/', views.eliminar_municipio, name='eliminar_municipio'),

    # 📌 CONDICIONES
    path('condiciones/', views.listar_condiciones, name='listar_condiciones'),
    path('condiciones/crear/', views.crear_condicion, name='crear_condicion'),
    path('condiciones/editar/<int:pk>/', views.editar_condicion, name='editar_condicion'),
    path('condiciones/eliminar/<int:pk>/', views.eliminar_condicion, name='eliminar_condicion'),
     # 📌 URLs para PROYECTOS
    path('proyectos/', views.listar_proyectos, name='listar_proyectos'),
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/editar/<int:pk>/', views.editar_proyecto, name='editar_proyecto'),
    path('proyectos/eliminar/<int:pk>/', views.eliminar_proyecto, name='eliminar_proyecto'),

    # 📌 URLs para AUTORIZACIONES
    path('autorizaciones/', views.listar_autorizaciones, name='listar_autorizaciones'),
    path('autorizaciones/crear/', views.crear_autorizacion, name='crear_autorizacion'),
    path('autorizaciones/editar/<int:pk>/', views.editar_autorizacion, name='editar_autorizacion'),
    path('autorizaciones/eliminar/<int:pk>/', views.eliminar_autorizacion, name='eliminar_autorizacion'),
    path("", views.inicio, name="inicio"),  # Página de inicio
    path("api/estadisticas/", views.api_estadisticas, name="api_estadisticas"),  # API para actualización

]
