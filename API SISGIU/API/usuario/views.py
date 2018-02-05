from django.shortcuts import render
from django.http import HttpResponse
from usuario.utils import render_to_pdf, date_handler
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json

from bson import json_util

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    )

from .permissions import (
    isOwnerOrReadOnly, 
    IsListOrCreate,
    )

from usuario.models import (
    Usuario,
    Estudiante,
    TipoPostgrado,
    EstadoEstudiante,
    PersonalDocente,
    PersonalAdministrativo,
    )
from usuario.serializers import (
    AdministradorListSerializer,
    AdministradorDetailSerializer,
    EstudianteSerializer,
    EstudianteDetailSerializer,
    TipoPostgradoSerializer,
    EstadoEstudianteSerializer,
    DocenteSerializer,
    DocenteDetailSerializer,
    AdministrativoSerializer,
    AdministrativoDetailSerializer
    )
from relacion.models import (
    EstudianteAsignatura,
    PeriodoEstudiante,
    )
from rest_framework.generics import (
	ListCreateAPIView,
	RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
	)


host_react = 'http://localhost:3000/'

"""
Usuario
"""
class AdministradorListCreateAPIView(ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = AdministradorListSerializer
    permission_classes = [IsAdminUser]

class AdministradorDetailAPIView(RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = AdministradorDetailSerializer
    lookup_field = 'cedula'
    permission_classes = [IsAdminUser]

    def get_usr_id(request, id_usr):
        if(request.user.is_anonymous == False):
            member = Usuario.objects.filter(id=id_usr)
            list_result = [entry for entry in member.values()]

            # Codigo para cambiar el username de un administrador.
            """
            user = Usuario.objects.get(id=id_usr)
            user.username = 24635907
            user.cedula = 24635907
            user.save()
            """

            return HttpResponse(json.dumps(list_result, default=date_handler), content_type="application/json")
        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta accion'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)


    @csrf_exempt
    def get_usr_cedula(request, cedula):
       
        if(request.method == "POST"):
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            cedula = body['cedula']
            password = body['password']
            nueva_contrasena = body['nueva_contrasena']

            user = Usuario.objects.get(cedula=cedula)
            if(user):
                if(password == user.password):
                    user.set_password(nueva_contrasena)
                    user.save()
                    status = 200
                else:
                    status = 404
            else:
                status = 404
           
            return HttpResponse(json.dumps({"Recuperacion":"OK"}, default=date_handler), content_type="application/json", status=status)

        member = Usuario.objects.filter(username=cedula)
        list_result = {"password": member.values()[0]['password']}

        return HttpResponse(json.dumps(list_result, default=date_handler), content_type="application/json")




    def send_mail(request, cedula):

        member = Usuario.objects.filter(username=cedula)
        if member:
            member = member.values()[0]
            correo = member['email']
            password = member['password']
            

            url = host_react + "recuperarContrasena/"+cedula+"/"+password;
            body = "Haga click en el siguiente enlace " + url +" para restablecer su contraseña"

            send_mail('Rescuperación de contraseña', body, 'sisgiu.fau@gmail.com', [correo])


            # Codigo para cambiar el username de un administrador.
            """
            user = Usuario.objects.get(id=id_usr)
            user.username = 24635907
            user.cedula = 24635907
            user.save()
            """
            response_data = {}
            response_data['status'] = 'Correo enviado'  

            return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
        
        response_data = {}
        response_data['error'] = 'Cedula no encontrada'  

        return HttpResponse(json.dumps(response_data), content_type="application/json", status=404)


class AdministradorUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = AdministradorDetailSerializer
    lookup_field = 'cedula'
    permission_classes = [IsAdminUser]

class AdministradorDeleteAPIView(DestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = AdministradorDetailSerializer
    lookup_field = 'cedula'
    permission_classes = [IsAdminUser]


"""
Estudiante
"""
class EstudianteListCreateAPIView(ListCreateAPIView):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated, IsListOrCreate]

class EstudianteDetailAPIView(RetrieveAPIView):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteDetailSerializer
    lookup_field = 'usuario__cedula'
    permission_classes = [IsAuthenticated]

    # def get_estudiante_asignatura(request, codigo_asignatura):


    def get_estudiantes_asignatura(request, codigo_asignatura):
        if (request.user.is_anonymous == False):
            member = EstudianteAsignatura.objects.filter(asignatura__codigo=codigo_asignatura, periodo_estudiante__periodo__estado_periodo__estado="activo").values()
            
            lista_estudiante_asignatura = [entry for entry in member]
            lista_periodo_estudiante = []
            lista_estudiantes = []

            for estudiante_asignatura in lista_estudiante_asignatura:
                periodo_estudiante = PeriodoEstudiante.objects.filter(id=estudiante_asignatura['periodo_estudiante_id']).values()[0]
                estudiante = Usuario.objects.filter(id=periodo_estudiante['estudiante_id']).values()[0]
                
                estudiante_asignatura['periodo_estudiante'] = periodo_estudiante
                estudiante_asignatura['estudiante'] = estudiante
                
                # periodo_estudiante['estudiante'] = estudiante

                # lista_periodo_estudiante.append(periodo_estudiante)

            for element in lista_estudiante_asignatura: 
                del element['estudiante']['sexo'] 
                del element['estudiante']['username'] 
                del element['estudiante']['date_joined'] 
                del element['estudiante']['last_login'] 
                del element['estudiante']['correo_alternativo'] 
                del element['estudiante']['is_active'] 
                del element['estudiante']['is_staff'] 
                del element['estudiante']['nacionalidad'] 
                del element['estudiante']['foto'] 
                del element['estudiante']['telefono_trabajo'] 
                del element['estudiante']['password'] 
                del element['estudiante']['estado_civil'] 
                del element['estudiante']['celular'] 
                del element['estudiante']['is_superuser'] 
                del element['estudiante']['email'] 
                del element['estudiante']['telefono_casa'] 
                del element['estudiante']['fecha_nacimiento'] 

            # print('--->' + str(lista_estudiante_asignatura))
            # print('###############\n\n')

            return HttpResponse(json.dumps(lista_estudiante_asignatura, default=date_handler), content_type="application/json")

        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta accion'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)



class EstudianteUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, isOwnerOrReadOnly]
    lookup_field = 'usuario__cedula'

class EstudianteDeleteAPIView(DestroyAPIView):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteDetailSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'usuario__cedula'



"""
TipoPostgrado
"""
class TipoPostgradoListCreateAPIView(ListCreateAPIView):
    queryset = TipoPostgrado.objects.all()
    serializer_class = TipoPostgradoSerializer
    permission_classes = [IsListOrCreate, IsAuthenticated]


class TipoPostgradoDeleteAPIView(DestroyAPIView):
    queryset = TipoPostgrado.objects.all()
    serializer_class = TipoPostgradoSerializer
    permission_classes = [IsAdminUser]


"""
EstadoEstudiante
"""
class EstadoEstudianteListCreateAPIView(ListCreateAPIView):
    queryset = EstadoEstudiante.objects.all()
    serializer_class = EstadoEstudianteSerializer
    permission_classes = [IsListOrCreate, IsAuthenticated]


class EstadoEstudianteDeleteAPIView(DestroyAPIView):
    queryset = EstadoEstudiante.objects.all()
    serializer_class = EstadoEstudianteSerializer
    permission_classes = [IsAdminUser]





"""
Docente
"""
class DocenteListCreateAPIView(ListCreateAPIView):
    queryset = PersonalDocente.objects.all()
    serializer_class = DocenteSerializer
    permission_classes = [IsAuthenticated, IsListOrCreate]

class DocenteDetailAPIView(RetrieveAPIView):
    queryset = PersonalDocente.objects.all()
    serializer_class = DocenteDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'usuario__cedula'


class DocenteUpdateAPIView(RetrieveUpdateAPIView):
    queryset = PersonalDocente.objects.all()
    serializer_class = DocenteDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, isOwnerOrReadOnly]
    lookup_field = 'usuario__cedula'

class DocenteDeleteAPIView(DestroyAPIView):
    queryset = PersonalDocente.objects.all()
    serializer_class = DocenteDetailSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'usuario__cedula'



"""
Personal Administrativo
"""
class AdministrativoListCreateAPIView(ListCreateAPIView):
    queryset = PersonalAdministrativo.objects.all()
    serializer_class = AdministrativoSerializer
    permission_classes = [IsAuthenticated, IsListOrCreate]

class AdministrativoDetailAPIView(RetrieveAPIView):
    queryset = PersonalAdministrativo.objects.all()
    serializer_class = AdministrativoDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'usuario__cedula'

class AdministrativoUpdateAPIView(RetrieveUpdateAPIView):
    queryset = PersonalAdministrativo.objects.all()
    serializer_class = AdministrativoDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, isOwnerOrReadOnly]
    lookup_field = 'usuario__cedula'

class AdministrativoDeleteAPIView(DestroyAPIView):
    queryset = PersonalAdministrativo.objects.all()
    serializer_class = AdministrativoDetailSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'usuario__cedula'



class Reportes():
    def report_test(request, cedula):
        if(request.user.is_anonymous != False):
            member = Usuario.objects.get(username=request.user)
            if(member.is_superuser == True or cedula == str(request.user.cedula)):
                content = 'attachment; filename="constancia_'+str(cedula)+'.pdf"'
                member = Usuario.objects.get(cedula=cedula)
                pdf = render_to_pdf('constancia.html', member.__dict__)
                pdf['Content-Disposition'] = content
                return HttpResponse(pdf, content_type='application/pdf')

        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta accion'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)