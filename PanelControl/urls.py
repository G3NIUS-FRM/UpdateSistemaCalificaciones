from django.urls import path
from . import views

urlpatterns=[
    path('',views.Home),
    path('salir/', views.salir, name="salir"),
    path('estudiantes/',views.obtenerEstudiantes,name="estudiantes_por_curso"),
    path("agregar_nota/",views.agregarNota,name="agregarNota"),
    path("editar_nota",views.editarNota,name="editar_nota"),
    path("actualizar_nota",views.actualizarNota,name="actualizar_panel"),
    path("apuntes/",views.Notas, name="apuntes")

]