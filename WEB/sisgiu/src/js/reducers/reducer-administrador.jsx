const initialState = {periodos: [], tiene_periodos_activos: true, periodo_terminado_error: false};

export default function (state=initialState, action) {

	switch (action.type){

		case "GET_PERIODOS_SUCCESS":
			return {
				periodos:action.payload['periodos'],
				tiene_periodos_activos: true 
			};
		case "SIN_PERIODOS_ACTIVOS":
			return {
				tiene_periodos_activos: false,
			};
		case "GET_PERIODOS_ERROR":
			return {
				loggedIn: false, 
			};

		case "PERIODO_TERMINADO_SUCCESS":
			return {
				periodo_terminado_error: false, 
				tiene_periodos_activos: true,
			};

		case "PERIODO_TERMINADO_ERROR":
			return {
				periodo_terminado_error: true, 
			};


		default:
			return state;
	}
}