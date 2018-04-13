from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from asignatura.models import (
	TipoAsignatura,
	Asignatura,
    PrelacionAsignatura,
	)

from usuario.models import(
    TipoPostgrado,
    Usuario,
    Estudiante
    )

from periodo.models import ( Periodo, )

from relacion.models import (
    DocenteAsignatura,
    EstudianteAsignatura,
    AsignaturaTipoPostgrado,
    PeriodoEstudiante,
    )
from asignatura.serializers import (
	TipoAsignaturaListSerializer,
	TipoAsignaturaDetailSerializer,
	AsignaturaListSerializer,
	AsignaturaDetailSerializer,
    PrelacionAsignaturaListSerializer
	)
from rest_framework.generics import (
	ListCreateAPIView,
	RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
	)

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

"""
TipoAsignatura
				Esto solo debe ser tratado por el administrador
"""
class TipoAsignaturaListCreateAPIView(ListCreateAPIView):
    queryset = TipoAsignatura.objects.all()
    serializer_class = TipoAsignaturaListSerializer
    permission_classes = [IsAuthenticated, IsListOrCreate]

class TipoAsignaturaDetailAPIView(RetrieveAPIView):
    queryset = TipoAsignatura.objects.all()
    serializer_class = TipoAsignaturaDetailSerializer
    permission_classes = [IsAuthenticated]

class TipoAsignaturaUpdateAPIView(RetrieveUpdateAPIView):
    queryset = TipoAsignatura.objects.all()
    serializer_class = TipoAsignaturaDetailSerializer
    permission_classes = [IsAdminUser]

class TipoAsignaturaDeleteAPIView(DestroyAPIView):
    queryset = TipoAsignatura.objects.all()
    serializer_class = TipoAsignaturaDetailSerializer
    permission_classes = [IsAdminUser]


"""
Asignatura
				Esto solo debe ser tratado por el administrador
"""
class AsignaturaListCreateAPIView(ListCreateAPIView):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsListOrCreate]

    def get_estudiantes_docente(request, codigo, tipo_postgrado):
        if(request.method == "GET"):
            member = EstudianteAsignatura.objects.filter(asignatura__codigo=codigo, periodo_estudiante__periodo__tipo_postgrado__tipo=tipo_postgrado, periodo_estudiante__periodo__estado_periodo__estado="activo").values()
            lista_estudiante_asignatura = [entry for entry in member]  # converts ValuesQuerySet into Python list

            lista_estudiantes = []

            for estudiante_asignatura in lista_estudiante_asignatura:
                periodo = PeriodoEstudiante.objects.filter(id=estudiante_asignatura['periodo_estudiante_id']).values()[0]

                estudiante = Usuario.objects.filter(id=periodo['estudiante_id']).values()[0]               

                estudiante_asignatura['first_name'] = estudiante['first_name']
                estudiante_asignatura['last_name'] = estudiante['last_name']
                estudiante_asignatura['cedula'] = estudiante['cedula'] 

                lista_estudiantes.append(estudiante_asignatura);

            return HttpResponse(json.dumps(lista_estudiantes), content_type="application/json")

        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta accion'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

    def get_asignaturas_por_docente(request, cedula):
        if (request.user.is_anonymous != False):
            member = DocenteAsignatura.objects.filter(docente__usuario__cedula=cedula , periodo__estado_periodo__estado="activo")
            # member = DocenteAsignatura.objects.filter(docente__usuario__cedula=cedula)



            member = member.values()
            print(member)
            lista_docente_asignatura = [entry for entry in member]  # converts ValuesQuerySet into Python list
            lista_asignaturas = []

            for docente_asignatura in lista_docente_asignatura:
                    asignatura = Asignatura.objects.filter(id=docente_asignatura['asignatura_id']).values()[0]               
                    periodo = Periodo.objects.filter(id=docente_asignatura['periodo_id']).values()[0]
                    tipo_postgrado = TipoPostgrado.objects.filter(id=periodo['tipo_postgrado_id']).values()[0]

                    if not (any(item['codigo'] == asignatura['codigo'] for item in lista_asignaturas)) or not (any(item['tipo_postgrado'] == tipo_postgrado['tipo'] for item in lista_asignaturas)):
                        tipo_asignatura = TipoAsignatura.objects.filter(id=asignatura['tipo_asignatura_id']).values()[0]

                        asignatura['tipo_asignatura'] = tipo_asignatura['nombre']
                        asignatura['tipo_postgrado'] = tipo_postgrado['tipo'];
                        asignatura['horario_dia'] = docente_asignatura['horario_dia']
                        asignatura['horario_hora'] = docente_asignatura['horario_hora']

                        del asignatura['tipo_asignatura_id']
                        lista_asignaturas.append(asignatura)

            return HttpResponse(json.dumps(lista_asignaturas), content_type="application/json")
        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta accion'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

    def get_asignaturas_por_estudiante(request, cedula):
        if (request.user.is_anonymous != False):

            estudiante = Estudiante.objects.get(usuario__cedula=cedula)

            member = EstudianteAsignatura.objects.filter(Q(periodo_estudiante__estudiante=estudiante) & (Q(periodo_estudiante__periodo__estado_periodo__estado='activo') | Q(periodo_estudiante__periodo__estado_periodo__estado='en inscripcion'))  ).values()

            lista_estudiante_asignatura = [entry for entry in member]

            lista_asignaturas = []

            for estudiante_asignatura in lista_estudiante_asignatura:

                asignatura = Asignatura.objects.filter(id=estudiante_asignatura['asignatura_id']).values()[0]
                tipo_asignatura = TipoAsignatura.objects.filter(id=asignatura['tipo_asignatura_id']).values()[0]

                # docente_asignatura = DocenteAsignatura.objects.filter(asignatura_id=asignatura['id'], periodo__estado_periodo__estado='activo', periodo__tipo_postgrado__tipo=estudiante.id_tipo_postgrado).values()
                docente_asignatura = DocenteAsignatura.objects.filter(Q(asignatura_id=asignatura['id']) & (Q(periodo__estado_periodo__estado='activo') | Q(periodo__estado_periodo__estado='en inscripcion') ) & Q(periodo__tipo_postgrado__tipo=estudiante.id_tipo_postgrado)).values()
                horarios_dia = []
                horarios_hora = []

                lista_docente_asignatura = [entry for entry in docente_asignatura]
                asignatura['docente'] = {}

                docente_informacion = Usuario.objects.filter(id=lista_docente_asignatura[0]['docente_id']).values()[0]
                asignatura['docente']['first_name'] = docente_informacion['first_name']
                asignatura['docente']['last_name'] = docente_informacion['last_name']

                for docente in lista_docente_asignatura:
                    horarios_dia.append(docente['horario_dia'])
                    horarios_hora.append(docente['horario_hora'])

                asignatura['docente']['horario_dia'] = horarios_dia
                asignatura['docente']['horario_hora'] = horarios_hora
                print(estudiante_asignatura)
                asignatura['retirado'] = estudiante_asignatura['retirado']

                asignatura['tipo_asignatura'] = tipo_asignatura['nombre']

                del asignatura['tipo_asignatura_id']

                lista_asignaturas.append(asignatura)

            lista_asignaturas = sorted(lista_asignaturas, key=lambda k: k['codigo']) 
            return HttpResponse(json.dumps(lista_asignaturas), content_type="application/json")
        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta accion'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

    def get_asignaturas(request):
        if (request.user.is_authenticated == True):
            member = Asignatura.objects.all().values()

            lista_asignaturas = [entry for entry in member]

            response_asignaturas = []

            for asignatura in lista_asignaturas:

                tipo_asignatura = TipoAsignatura.objects.filter(id=asignatura['tipo_asignatura_id']).values()[0]
                asignatura['tipo_asignatura'] = tipo_asignatura['nombre']

                response_asignaturas.append(asignatura)

            return HttpResponse(json.dumps(response_asignaturas), content_type="application/json")
        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta acción'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

    @csrf_exempt
    def retirar_periodo_estudiante(request, cedula, periodo):
        if (request.method == 'POST'):

            member = EstudianteAsignatura.objects.filter(
                periodo_estudiante__estudiante__usuario__cedula=cedula,
                periodo_estudiante__periodo_id=periodo).update(retirado=True)

            response_data = {}
            response_data['status'] = 'Edicion exitosa'      
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta acción'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)


class AsignaturaDetailAPIView(RetrieveAPIView):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'codigo'


class AsignaturaUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaDetailSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'codigo'


class AsignaturaDeleteAPIView(DestroyAPIView):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaDetailSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'codigo'


"""
PrelacionAsignatura
                Esto solo debe ser tratado por el administrador
"""


class PrelacionAsignaturaListCreateAPIView(ListCreateAPIView):
    queryset = PrelacionAsignatura.objects.all()
    serializer_class = PrelacionAsignaturaListSerializer

    @csrf_exempt
    def post_prelacion(request):
        if (request.method == 'POST'):
            codigos=json.loads(request.body.decode("utf-8"))
            PrelacionAsignatura.objects.filter(asignatura_objetivo=codigos['codigo']).delete()
            prelacion = []
            for code in codigos['prelaciones']:
                prelacion = PrelacionAsignatura.objects.create(
                    asignatura_objetivo=Asignatura.objects.get(codigo = codigos['codigo']), 
                    asignatura_prela=Asignatura.objects.get(codigo = code))

            response_data = {}
            response_data['status'] = 'Creacion exitosa'      
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta acción'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)


    def get_asignaturas_necesarias(request, codigo):
        if (request.method == 'GET'):
            
            asignaturas = PrelacionAsignatura.objects.filter(asignatura_objetivo=codigo).values()

            lista_prelaciones = [entry for entry in asignaturas]

            lista_asignaturas = []

            for prelacion in lista_prelaciones:
                asignatura = Asignatura.objects.filter(codigo=prelacion['asignatura_objetivo_id']).values()[0]
                prelacion['nombre_asignatura_objetivo'] = asignatura['nombre']
                
                asignatura = Asignatura.objects.filter(codigo=prelacion['asignatura_prela_id']).values()[0]
                prelacion['nombre_asignatura_prela'] = asignatura['nombre']

                lista_asignaturas.append(prelacion)

            return HttpResponse(json.dumps(lista_asignaturas), content_type="application/json")

        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta acción'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

    def get_all_asignaturas_necesarias(request):
        if (request.method == 'GET'):
            
            asignaturas = PrelacionAsignatura.objects.all().values()

            lista_prelaciones = [entry for entry in asignaturas]

            
            lista_asignaturas = []

            for prelacion in lista_prelaciones:
                asignatura = Asignatura.objects.filter(codigo=prelacion['asignatura_objetivo_id']).values()[0]
                prelacion['nombre_asignatura_objetivo'] = asignatura['nombre']
                
                asignatura = Asignatura.objects.filter(codigo=prelacion['asignatura_prela_id']).values()[0]
                prelacion['nombre_asignatura_prela'] = asignatura['nombre']

                lista_asignaturas.append(prelacion)
     
            return HttpResponse(json.dumps(lista_asignaturas), content_type="application/json")

        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta acción'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

    @csrf_exempt
    def delete_asignaturas_necesarias(request, codigo):
        if (request.method == "DELETE"):
            
            asignaturas = PrelacionAsignatura.objects.filter(asignatura_objetivo=codigo).delete()

            response_data = {}
            response_data['status'] = 'Eliminacion exitosa'  
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta acción'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

    @csrf_exempt
    def delete_all_asignaturas_necesarias(request):
        if (request.method == "DELETE"):
            
            asignaturas = PrelacionAsignatura.objects.all().delete()

            response_data = {}
            response_data['status'] = 'Eliminacion exitosa'  
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta acción'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)


    def get_asignaturas_a_inscribir(request, cedula):

        if (request.method == 'GET'):

            # Lista de todas las asignaturas en el sistema
            asignaturas = Asignatura.objects.all()

            # Estudiante al cual se le buscan las asignaturas
            estudiante = Estudiante.objects.get(usuario__cedula=cedula)

            # Lista de todos los periodos que ha cursado el estudiante
            periodo_estudiante = PeriodoEstudiante.objects.filter(estudiante=estudiante)
            # print(periodo_estudiante, '\n')

            # Lista de todos los codigos de las asignaturas que ya se cursaron
            lista_asignaturas_cursadas = []
            for x in periodo_estudiante:
                estudiante_asignatura = EstudianteAsignatura.objects.filter(periodo_estudiante=x, nota_definitiva__gte=10, retirado=False)
                for y in estudiante_asignatura:
                    lista_asignaturas_cursadas.append(y.asignatura.codigo)

            print('ya se cursaron -> ', lista_asignaturas_cursadas,'\n')
            
            # Convierto el QuerySet de Asignaturas en un JSON
            asignaturas = [entry for entry in asignaturas.values()]

            lista_codigos_asignaturas = []

            for x in asignaturas:
                # Si la asignatura no se ha cursado, se agrega a la lista
                if (x['codigo'] not in lista_asignaturas_cursadas):
                    lista_codigos_asignaturas.append(x['codigo'])

            # Busco en la lista las asignaturas que aun no pueden verse porque estan preladas por otras
            lista_eliminar = []
            lista_codigo_asignaturas_a_inscribir = []

            for x in lista_codigos_asignaturas:
                aux = PrelacionAsignatura.objects.filter(asignatura_prela__codigo=x)
                aux = [entry for entry in aux.values()]

                for y in aux:
                    lista_eliminar.append( y['asignatura_objetivo_id'] )

            print('Aun no se pueden cursar  -> ', lista_eliminar,'\n')
            
            # Construyo la lista final 
            for x in lista_codigos_asignaturas:
                if (x not in lista_eliminar):
                    lista_codigo_asignaturas_a_inscribir.append(x)

            print('lista_codigo_asignaturas_a_inscribir = ', lista_codigo_asignaturas_a_inscribir,'\n')


            periodo = Periodo.objects.get(estado_periodo_id__estado='en inscripcion', tipo_postgrado_id__tipo=estudiante.id_tipo_postgrado)

            asignaturas_id = DocenteAsignatura.objects.filter(periodo=periodo).values('asignatura')

            lista_codigos_en_periodo_a_inscribir = []

            for x in asignaturas_id:
                asignatura = Asignatura.objects.get(id=x['asignatura'])
                print(asignatura)
                print(asignatura.codigo)

                if (asignatura.codigo in lista_codigo_asignaturas_a_inscribir):
                    lista_codigos_en_periodo_a_inscribir.append(asignatura.codigo)


                print('##############################')

            n = len(asignaturas)
            lista_asignaturas_a_inscribir = []

            for i in range(0, n):
                if ( asignaturas[i]['codigo'] in lista_codigos_en_periodo_a_inscribir ):
                    lista_asignaturas_a_inscribir.append(asignaturas[i])

            print(lista_asignaturas_a_inscribir)

            return HttpResponse(json.dumps(lista_asignaturas_a_inscribir), content_type="application/json", status=200)




        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta acción'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)


    def get_asignaturas_actuales_estudiante(request, cedula):

        if (request.method == 'GET'):

            # Estudiante al cual se le buscan las asignaturas
            estudiante = Estudiante.objects.get(usuario__cedula=cedula)

            # El PeriodoEstudiante actual
            periodo_estudiante = PeriodoEstudiante.objects.get(Q(estudiante=estudiante) & (Q(periodo__estado_periodo__estado='activo') | Q(periodo__estado_periodo__estado='en inscripcion'))  )
            
            estudiante_asignatura = EstudianteAsignatura.objects.filter(periodo_estudiante_id=periodo_estudiante.id).values()

            lista_asignaturas=[]
            for x in estudiante_asignatura:
                asignatura = Asignatura.objects.filter(id=x['asignatura_id']).values()[0]
                lista_asignaturas.append(asignatura);

            return HttpResponse(json.dumps(lista_asignaturas), content_type="application/json", status=200)

        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta acción'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)


    def get_asignaturas_actuales(request, periodo):

        if (request.method == 'GET'):

            # El DocenteAsignaturas del periodo actual
            docente_asignatura = DocenteAsignatura.objects.filter(periodo_id=periodo).values()

            lista_asignaturas=[]
            for x in docente_asignatura:
                asignatura = Asignatura.objects.filter(id=x['asignatura_id']).values()[0]
                lista_asignaturas.append(asignatura);

            return HttpResponse(json.dumps(lista_asignaturas), content_type="application/json", status=200)

        response_data = {}
        response_data['error'] = 'No tiene privilegios para realizar esta acción'      
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=401)

