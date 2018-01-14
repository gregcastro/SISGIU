from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from relacion.views import (
	
	PeriodoEstudianteListCreateAPIView,
	PeriodoEstudianteDetailAPIView,
	PeriodoEstudianteUpdateAPIView,
	PeriodoEstudianteDeleteAPIView,
	DocenteAsignaturaListCreateAPIView,
	DocenteAsignaturaDetailAPIView,
	DocenteAsignaturaUpdateAPIView,
	DocenteAsignaturaDeleteAPIView,
	EstudianteAsignaturaListCreateAPIView,
	EstudianteAsignaturaDetailAPIView,
	EstudianteAsignaturaUpdateAPIView,
	EstudianteAsignaturaDeleteAPIView,
	EstudianteTramiteListCreateAPIView,
	EstudianteTramiteDetailAPIView,
	EstudianteTramiteUpdateAPIView,
	EstudianteTramiteDeleteAPIView,
	AsignaturaTipoPostgradoListCreateAPIView,
	AsignaturaTipoPostgradoDetailAPIView,
	AsignaturaTipoPostgradoUpdateAPIView,
	AsignaturaTipoPostgradoDeleteAPIView,
	
	)


urlpatterns = format_suffix_patterns([

	# PeriodoEstudiante
    url(r'^api/periodoEstudiante/$', PeriodoEstudianteListCreateAPIView.as_view(), name='PeriodoEstudiante-list-create'),
    url(r'^api/periodoEstudiante/(?P<pk>\d+)/$', PeriodoEstudianteDetailAPIView.as_view(), name='PeriodoEstudiante-detail'),
    url(r'^api/periodoEstudiante/(?P<pk>\d+)/edit/$', PeriodoEstudianteUpdateAPIView.as_view(), name='PeriodoEstudiante-update'),
    url(r'^api/periodoEstudiante/(?P<pk>\d+)/delete/$', PeriodoEstudianteDeleteAPIView.as_view(), name='PeriodoEstudiante-delete'),

   
    # DocenteAsignatura
    url(r'^api/docenteAsignatura/$', DocenteAsignaturaListCreateAPIView.as_view(), name='DocenteAsignatura-list-create'),
    url(r'^api/docenteAsignatura/(?P<pk>\d+)/$', DocenteAsignaturaDetailAPIView.as_view(), name='DocenteAsignatura-detail'),
    url(r'^api/docenteAsignatura/(?P<pk>\d+)/edit/$', DocenteAsignaturaUpdateAPIView.as_view(), name='DocenteAsignatura-update'),
    url(r'^api/docenteAsignatura/(?P<pk>\d+)/delete/$', DocenteAsignaturaDeleteAPIView.as_view(), name='DocenteAsignatura-delete'),


    # EstudianteAsignatura
    url(r'^api/estudianteAsignatura/$', EstudianteAsignaturaListCreateAPIView.as_view(), name='EstudianteAsignatura-list-create'),
    url(r'^api/estudianteAsignatura/(?P<pk>\d+)/$', EstudianteAsignaturaDetailAPIView.as_view(), name='EstudianteAsignatura-detail'),
    url(r'^api/estudianteAsignatura/(?P<pk>\d+)/edit/$', EstudianteAsignaturaUpdateAPIView.as_view(), name='EstudianteAsignatura-update'),
    url(r'^api/estudianteAsignatura/(?P<pk>\d+)/delete/$', EstudianteAsignaturaDeleteAPIView.as_view(), name='EstudianteAsignatura-delete'),


    # EstudianteTramite
    url(r'^api/estudianteTramite/$', EstudianteTramiteListCreateAPIView.as_view(), name='EstudianteTramite-list-create'),
    url(r'^api/estudianteTramite/(?P<pk>\d+)/$', EstudianteTramiteDetailAPIView.as_view(), name='EstudianteTramite-detail'),
    url(r'^api/estudianteTramite/(?P<pk>\d+)/edit/$', EstudianteTramiteUpdateAPIView.as_view(), name='EstudianteTramite-update'),
    url(r'^api/estudianteTramite/(?P<pk>\d+)/delete/$', EstudianteTramiteDeleteAPIView.as_view(), name='EstudianteTramite-delete'),


    # AsignaturaTipoPostgrado
    url(r'^api/asignaturaTipoPostgrado/$', AsignaturaTipoPostgradoListCreateAPIView.as_view(), name='AsignaturaTipoPostgrado-list-create'),
    url(r'^api/asignaturaTipoPostgrado/(?P<pk>\d+)/$', AsignaturaTipoPostgradoDetailAPIView.as_view(), name='AsignaturaTipoPostgrado-detail'),
    url(r'^api/asignaturaTipoPostgrado/(?P<pk>\d+)/edit/$', AsignaturaTipoPostgradoUpdateAPIView.as_view(), name='AsignaturaTipoPostgrado-update'),
    url(r'^api/asignaturaTipoPostgrado/(?P<pk>\d+)/delete/$', AsignaturaTipoPostgradoDeleteAPIView.as_view(), name='AsignaturaTipoPostgrado-delete'),


])