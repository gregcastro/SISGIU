import { combineReducers } from 'redux';
import ActiveUserReducer from './reducer-active-user';
import DocenteReducer from './reducer-docente-user';
import RecuperarContrasena from './reducer-olvido-contrasena';
import EstudianteReducer from './reducer-estudiante';
import EditUserReducer from './reducer-edit-user';
import AdminReducer from './reducer-administrador';
import PaginacionReducer from './reducer-paginacion';
import AdministrativoUser from './reducer-administrativo';

/*
 * Combinamos todos los reducers en un solo objeto para enviar al store
 * Todos los estados de la aplicacion son los reducers que son retornados hacia la aplicacion
 * */



const allReducers = combineReducers({
	activeUser: ActiveUserReducer,
	adminUser: AdminReducer,
	estudianteUser: EstudianteReducer,
	docenteUser: DocenteReducer,
	administrativoUser: AdministrativoUser,
	editUser: EditUserReducer,
	recuperarContrasena: RecuperarContrasena,
	paginacion: PaginacionReducer,
});

const combineReducers_test = (state, action) => {
	if (action.type === 'LOGOUT_SUCCESS') {
		state = undefined;
	}
	return allReducers(state, action)
}

export default combineReducers_test