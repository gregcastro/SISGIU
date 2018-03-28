const initialState = {
	materias: [], 
	tiene_asignaturas: true,
	lista_periodo_estudiante: [],
	lista_periodos: [],
	first_render: false,
	lista_asignaturas_inscripcion: [],
	inscripcion_exitosa: false,
	error_inscripcion: false,

};

export default function (state=initialState, action) {

	var nuevo_estado = Object.assign({}, state);
	switch (action.type){

		case "GET_INFORMATION_SUCCESS":
			nuevo_estado['materias'] = action.payload['materias'];
			nuevo_estado['tiene_asignaturas'] = true;
			return nuevo_estado;

		case "GET_INFORMATION_ERROR":
			nuevo_estado['loggedIn'] = false;
			return nuevo_estado;

		case "ESTUDIANTE_SIN_ASIGNATURA":
			nuevo_estado['tiene_asignaturas'] = false;
			nuevo_estado['materias'] = [];
			return nuevo_estado;

		case "GET_PERIODO_ESTUDIANTE":
			nuevo_estado['lista_periodo_estudiante'] = action.payload['lista_periodo_estudiante'];
			nuevo_estado['first_render'] = true;
			return nuevo_estado;

		case "GET_PERIODOS_TIPO_POSTGRADO_EXITOSO":
			nuevo_estado['lista_periodos'] = action.payload['lista_periodos'];
			return nuevo_estado;

		case "ERROR":
			nuevo_estado['loggedIn'] = false;
			nuevo_estado['loading'] = false;
			return nuevo_estado;
		
		case "GET_ASIGNATURAS_INSCRIPCION_EXITOSO":
			nuevo_estado['lista_asignaturas_inscripcion'] = action.payload['lista_asignaturas_inscripcion'];
			return nuevo_estado;

		case "INSCRIPCION_EXITOSA":
			nuevo_estado['inscripcion_exitosa'] = true
			nuevo_estado['error_inscripcion'] = false
			return nuevo_estado;

		case "ERROR_INSCRIPCION":
			nuevo_estado['error_inscripcion'] = true
			nuevo_estado['inscripcion_exitosa'] = false
			return nuevo_estado;



		default:
			return state;
	}
}