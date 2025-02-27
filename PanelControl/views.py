from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
@login_required

def Home(request):
    
    print("Usuario autenticado:", request.user.is_authenticated)
    print("Usuario:", request.user)

    
    profesor = Profesores.objects.filter(Profesor=request.user).first()
    if profesor:
        # Obtener los cursos del profesor
        request.session["materia"] = profesor.Materia.id
        profesor_id=profesor.id
        request.session["profesor"]=profesor_id


        CursosProfe = profesor.Cursos.all()
    else:
        request.session["materia"]=None
        CursosProfe = []  # Si no se encuentra el profesor, no hay cursos


    return render(request, "index.html", {
        "Cursos": CursosProfe,
        "user":request.user
    })
def salir(request):
    logout(request)
    return redirect('/')
def CargarTabla(curso_id,materia):
    estudiantes=[]
    calificacion_estudiantes=[]
    estudiantes=Estudiantes.objects.filter(Curso=curso_id)
    for estudiante in estudiantes:
            calificaciones=Calificaciones.objects.filter(Estudiante=estudiante, Materia=materia)
            f=calificaciones.values()
            if f.exists():
                for calificacion in f:
                    c=calificacion["Calificacion"]
                    calificacion_estudiantes.append(c)
            else:
                calificacion_estudiantes.append(1)
                    
                    
            print(calificacion_estudiantes)
                    
    ec = [(estudiante.Nombre, calificacion) for estudiante, calificacion in zip(estudiantes, calificacion_estudiantes)]
    return ec
def obtenerEstudiantes(request):
    cursos=Cursos.objects.all()
    

    curso_id=request.GET.get('curso')
    request.session["curso"]=curso_id
    materia=request.session.get("materia")
    if not materia:  # Si no hay materia en la sesión, redirigir
        return redirect('/')
    try:
        materia=Materias.objects.get(id=materia)

    except materia.DoesNotExist:
        return redirect('/')

    
    if curso_id:
        ec=CargarTabla(curso_id,materia)
        request.session["ec"]=ec
    
 

            

        return render(request, "estudiantes.html", {'cursos': cursos, 'estudiantes_calificaciones': ec})

    return render(request, "estudiantes.html", {'cursos': cursos, 'estudiantes_calificaciones': []})
       
def agregarNota(request):
    ec=request.session.get("ec")
    if request.method == "POST":
        estudiante=request.POST.get("estudiante_id")
        calificion=request.POST.get("calificacion_id")
        e=Estudiantes.objects.filter(Nombre=estudiante).values().get()
        materia=request.session.get("materia")
        print(materia)
        print(e["Nombre"])
        print(Calificaciones.objects.filter(Estudiante_id=e["id"],Materia=materia))

        request.session["id"]=e
    return render(request, "estudiantes.html",{'estudiantes_calificaciones':ec,'estudiante_en_proceso':estudiante,"calificacion_en_proceso":calificion})

def editarNota(request):
    ec=request.session.get("ec")
    if request.method == "POST":
        estudiante=request.POST.get("estudiante_id")
        calificion=request.POST.get("calificacion_id")

        request.session["old_cali"]=calificion
        e=Estudiantes.objects.filter(Nombre=estudiante).values().get()
        

        request.session["id"]=e
        print(estudiante)
    return render(request, "estudiantes.html",{'estudiantes_calificaciones':ec,'estudiante_en_proceso':estudiante,"calificacion_en_proceso":calificion})
def actualizarNota(request):

    if request.method=="POST":
        curso_actual=request.session.get("curso")
        new_cali=request.POST.get("newCali")
        old_cali=request.session.get("old_cali")
        id=request.session.get("id")
        materia=request.session.get("materia")
        profesor=request.session.get("profesor")
        
        print(materia)
        print(id)
        if new_cali == old_cali:
            print("No se han cambiado los valores")
        else:
            cambios=Calificaciones.objects.filter(Estudiante_id=id["id"],Materia_id=materia)
            if cambios:
                cambios.update(Calificacion=new_cali)
                historial=Historial(Maestro_id=profesor, Estudiante_id=id["id"],Old=old_cali, New=new_cali,Cambio="Edicion").save()
            else:
                a=Calificaciones(Estudiante_id=id["id"],Periodo=1,Materia_id=materia,Calificacion=new_cali).save()
                historial=Historial(Maestro_id=profesor,Estudiante_id=id["id"],Old=old_cali, New=new_cali,Cambio="Edicion").save()
    ec=CargarTabla(curso_actual,materia)


    return render(request, "estudiantes.html", {"estudiantes_calificaciones":ec})
def Notas(request):
    return render(request, "notas.html")