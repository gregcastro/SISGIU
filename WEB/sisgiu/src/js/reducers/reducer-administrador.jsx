const initialState = {
	edit: false,
	create: false,
	tiene_periodos_activos: true,
	periodo_terminado_error: false,
	lista_usuarios: [],
	bad_input: false,
	lista_asignaturas: [],
	lista_postgrados: [],
	lista_periodos: [],
	lista_tipoAsignaturas: [],
	lista_estadoEstudiante: [],
	lista_estadoPeriodo: [],
	lista_prelacion: [],
	lista_docente_asignatura: [],
	error_creando_periodo: false,
	error_docente_tipo_postgrado: false,
	periodo_en_inscripcion_repetido: false,
};

export default function (state = initialState, action) {
	var nuevo_estado = Object.assign({}, state);

	switch (action.type) {


		// Global
		case "HIDE_ALERTS":
			nuevo_estado['edit'] = false;
			nuevo_estado['bad_input'] = false;
			nuevo_estado['create'] = false;
			nuevo_estado['error_docente_tipo_postgrado'] = false;
			nuevo_estado['error_creando_periodo'] = false;
			nuevo_estado['periodo_en_inscripcion_repetido'] = false;
			return nuevo_estado;

		case "ERROR":
			nuevo_estado['loggedIn'] = false;
			return nuevo_estado;


		// Modulo INICIO
		case "PERIODO_TERMINADO_SUCCESS":
			nuevo_estado['periodo_terminado_error'] = false;
			nuevo_estado['tiene_periodos_activos'] = true;
			return nuevo_estado;

		case "PERIODO_TERMINADO_ERROR":
			nuevo_estado['periodo_terminado_error'] = true;
			return nuevo_estado;

		case "GET_PERIODOS_ACTIVOS_EXITOSO":
			nuevo_estado['lista_periodos'] = action.payload['periodos'];
			nuevo_estado['tiene_periodos_activos'] = true;
			nuevo_estado['edit'] = false;
			return nuevo_estado;

		case "SIN_PERIODOS_ACTIVOS":
			nuevo_estado['tiene_periodos_activos'] = false;
			nuevo_estado['lista_periodos'] = action.payload['periodos'];
			return nuevo_estado;


		// Modulo USUARIOS
		case "CREATE_USER_SUCCESS":
			nuevo_estado['create'] = true;
			nuevo_estado['edit'] = false;
			nuevo_estado['bad_input'] = false;
			nuevo_estado['error_docente_tipo_postgrado'] = false;
			nuevo_estado['lista_usuarios'] = action.payload['lista_usuarios'];
			return nuevo_estado;

		case "GET_USUARIOS_EXITOSO":
			nuevo_estado['lista_usuarios'] = action.payload['lista_usuarios'];
			return nuevo_estado;

		case "GET_ESTADO_ESTUDIANTE_EXITOSO":
			nuevo_estado['lista_estadoEstudiante'] = action.payload['lista_estadoEstudiante'];
			return nuevo_estado;

		case "EDIT_USER_INFO_SUCCESS":
			nuevo_estado['bad_input'] = false;
			nuevo_estado['create'] = false;
			nuevo_estado['edit'] = true;
			nuevo_estado['error_docente_tipo_postgrado'] = false;
			nuevo_estado['lista_usuarios'] = action.payload['lista_usuarios'];
			return nuevo_estado;

		case "EDIT_USER_INFO_ERROR":
			nuevo_estado['bad_input'] = true;
			nuevo_estado['create'] = false;
			nuevo_estado['edit'] = false;
			nuevo_estado['error_docente_tipo_postgrado'] = false;
			nuevo_estado['lista_usuarios'] = action.payload['lista_usuarios'];
			return nuevo_estado;

		case "ERROR_DOCENTE_TIPO_POSTGRADO":
			nuevo_estado['create'] = false;
			nuevo_estado['edit'] = false;
			nuevo_estado['bad_input'] = false;
			nuevo_estado['error_docente_tipo_postgrado'] = true;
			nuevo_estado['lista_usuarios'] = action.payload['lista_usuarios'];
			return nuevo_estado;


		// Modulo ASIGNATURAS
		case "CREAR_ASIGNATURA_EXITOSO":
			nuevo_estado['create'] = true;
			nuevo_estado['edit'] = false;
			nuevo_estado['bad_input'] = false;
			nuevo_estado['lista_asignaturas'] = action.payload['lista_asignaturas'];
			nuevo_estado['lista_prelacion'] = action.payload['lista_prelacion'];
			return nuevo_estado;

		case "ASIGNATURAS_ERROR":
			nuevo_estado['lista_asignaturas'] = action.payload['lista_asignaturas'];
			nuevo_estado['lista_prelacion'] = action.payload['lista_prelacion'];
			nuevo_estado['bad_input'] = true;
			nuevo_estado['create'] = false;
			nuevo_estado['edit'] = false;
			return nuevo_estado;

		case "GET_TIPO_ASIGNATURA_EXITOSO":
			nuevo_estado['lista_tipoAsignaturas'] = action.payload['lista_tipoAsignaturas'];
			return nuevo_estado;

		case "EDIT_ASIGNATURA_EXITOSO":
			nuevo_estado['edit'] = true;
			nuevo_estado['bad_input'] = false;
			nuevo_estado['create'] = false;
			nuevo_estado['lista_asignaturas'] = action.payload['lista_asignaturas'];
			nuevo_estado['lista_prelacion'] = action.payload['lista_prelacion'];
			return nuevo_estado;

		case "GET_ASIGNATURAS_EXITOSO":
			nuevo_estado['lista_asignaturas'] = action.payload['lista_asignaturas'];
			nuevo_estado['lista_prelacion'] = action.payload['lista_prelacion'];
			nuevo_estado['edit'] = false;
			nuevo_estado['create'] = false;
			nuevo_estado['bad_input'] = false;
			return nuevo_estado;


		// Modulo PERIODO
		case "PERIODO_EN_INSCRIPCION_REPETIDO":
			nuevo_estado['create'] = false;
			nuevo_estado['edit'] = false;
			nuevo_estado['bad_input'] = false;
			nuevo_estado['periodo_en_inscripcion_repetido'] = true;
			nuevo_estado['lista_periodos'] = action.payload['lista_periodos'];
			return nuevo_estado;

		case "CREATE_PERIODO_EXITOSO":
			nuevo_estado['create'] = true;
			nuevo_estado['edit'] = false;
			nuevo_estado['bad_input'] = false;
			nuevo_estado['error_creando_periodo'] = false;
			nuevo_estado['periodo_en_inscripcion_repetido'] = false;
			nuevo_estado['lista_periodos'] = action.payload['lista_periodos'];
			return nuevo_estado;

		case "GET_PERIODOS_EXITOSO":
			nuevo_estado['edit'] = false;
			nuevo_estado['bad_input'] = false;
			nuevo_estado['loading'] = false;
			nuevo_estado['create'] = false;
			nuevo_estado['periodo_en_inscripcion_repetido'] = false;
			nuevo_estado['error_creando_periodo'] = false;
			nuevo_estado['lista_periodos'] = action.payload['lista_periodos'];
			return nuevo_estado;

		case "EDIT_PERIODO_EXITOSO":
			nuevo_estado['edit'] = true;
			nuevo_estado['bad_input'] = false;
			nuevo_estado['create'] = false;
			nuevo_estado['periodo_en_inscripcion_repetido'] = false;
			nuevo_estado['error_creando_periodo'] = false;
			nuevo_estado['lista_periodos'] = action.payload['lista_periodos'];
			return nuevo_estado;

		case "PERIODO_ERROR":
			nuevo_estado['bad_input'] = true;
			nuevo_estado['loading'] = false;
			nuevo_estado['edit'] = false;
			nuevo_estado['create'] = false;
			nuevo_estado['periodo_en_inscripcion_repetido'] = false;
			nuevo_estado['error_creando_periodo'] = true;
			nuevo_estado['lista_periodos'] = action.payload['lista_periodos'];
			return nuevo_estado;

		case "ERROR_CREANDO_PERIODO":
			nuevo_estado['error_creando_periodo'] = true;
			nuevo_estado['periodo_en_inscripcion_repetido'] = false;
			nuevo_estado['create'] = false;
			nuevo_estado['edit'] = false;
			nuevo_estado['bad_input'] = false;
			return nuevo_estado;

		case "CREAR_DOCENTE_ASIGNATURA_EXITOSO":
			nuevo_estado['edit'] = true;
			nuevo_estado['bad_input'] = false;
			nuevo_estado['error_creando_periodo'] = false;
			nuevo_estado['periodo_en_inscripcion_repetido'] = false;
			nuevo_estado['create'] = false;
			return nuevo_estado;

		case "GET_DOCENTE_ASIGNATURA_EXITOSO":
			nuevo_estado['lista_docente_asignatura'] = action.payload['lista_docente_asignatura'];
			return nuevo_estado;

		case "GET_ESTADO_PERIODO_EXITOSO":
			nuevo_estado['lista_estadoPeriodo'] = action.payload['lista_estadoPeriodo'];
			return nuevo_estado;

		case "GET_TIPOS_POSTGRADO_EXITOSO":
			nuevo_estado['lista_postgrados'] = action.payload['lista_postgrados'];
			return nuevo_estado;
		
		
			default:
			return state;
	}
}