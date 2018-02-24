import request from 'superagent';
import jwt_decode from 'jwt-decode';
import {host} from '../components/globalVariables';
import mergeJSON from 'merge-json';


export function get_usuarios (tipo_usuario, edit) {
	let token = localStorage.getItem('user_token');

	try{
		jwt_decode(token);
	}catch(e){
		localStorage.removeItem('user_token');
		localStorage.removeItem('modulo');
		return {
			type: "ERROR"
		}
	}
	return request
	   .get(host+'api/usuarios/'+tipo_usuario+'/')
	   .set('Authorization', 'JWT '+token)
	   .then(function(res) {
	   		if(edit === 1){
	   			return {
					type: "EDIT_USER_INFO_SUCCESS",
					payload: {lista_usuarios: res.body}
				}
	   		}else if(edit === 2){
	   			return {
					type: "EDIT_USER_INFO_ERROR",
					payload: {lista_usuarios: res.body}
				}
	   		}
	   		else{
	   			return {
					type: "GET_USUARIOS_EXITOSO",
					payload: {lista_usuarios: res.body}
				}
	   		}

	   })
	   .catch(function(err) {
	   		localStorage.removeItem('user_token');
	   		localStorage.removeItem('modulo');
	      	return {
				type: "ERROR"
			}
	   });

}


export const editarUsuario = (cambios, user, tipo_usuario) => {
	let token = localStorage.getItem('user_token');
	let usuario = {
		"usuario": user
	}

	var result = mergeJSON.merge(usuario, cambios);
	delete result.usuario.foto;
	delete result.rif;
	delete result.curriculum;
	delete result.permiso_ingresos;
	console.log(result);
	return request
	   .put(host+'api/'+tipo_usuario+'/'+usuario['usuario']['cedula']+'/edit/')
	   .set('Authorization', 'JWT '+token)
	   .set('Content-Type', 'application/json')
	   .send(result)
	   .then(function(res) {
	   	console.log(res.body);
		   	  	return function (dispatch) {
				    dispatch(get_usuarios(tipo_usuario ,1));
				}

	   })
	   .catch(function(err) {
	   	console.log(err)
	   	  	return function (dispatch) {
			    dispatch(get_usuarios(tipo_usuario ,2));
			}
	   });
}


export const editarDocumento = (tipo_documento, documento, cedula) => {
    const formData = new FormData();
    formData.append(tipo_documento ,documento);
    console.log(formData.values());
	// let modulo = localStorage.getItem('modulo');
	let token = localStorage.getItem('user_token');
	// alert(cedula);
	return request
	   .post(host+'api/docentes/'+cedula+'/cambiarDocumento/'+tipo_documento+'/')
	   .set('Authorization', 'JWT '+token)
	   .field('username', cedula)
	   .field(tipo_documento, documento)
	   .then(function(res) {
		   	  	return function (dispatch) {
				    dispatch(get_usuarios("docentes" ,1));
				}
	   })
	   .catch(function(err) {
	   	console.log(err);
	   	  	return function (dispatch) {
			    dispatch(get_usuarios("docentes" ,2));
			}
	   });
}



export const crearUsuario = (user, tipo_usuario) => {
	let token = localStorage.getItem('user_token');
	user['usuario']['password'] = user['usuario']['cedula'];
	user['usuario']['username'] = user['usuario']['cedula'];
 	console.log(user);
	return request
	   .post(host+'api/'+tipo_usuario+'/')
	   .set('Authorization', 'JWT '+token)
	   .set('Content-Type', 'application/json')
	   .send(user)
	   .then(function(res) {
		   	  	return function (dispatch) {
				    dispatch(get_usuarios(tipo_usuario ,1));
				}

	   })
	   .catch(function(err) {
	   	console.log(err)
	   	  	return function (dispatch) {
			    dispatch(get_usuarios(tipo_usuario ,2));
			}
	   });
}




export const eliminarUsuario = (cedula, tipo_usuario) => {
	let token = localStorage.getItem('user_token');
	return request
	   .delete(host+'api/'+tipo_usuario+'/'+cedula+'/delete/')
	   .set('Authorization', 'JWT '+token)
	   .then(function(res) {
		   	  	return function (dispatch) {
				    dispatch(get_usuarios(tipo_usuario ,1));
				}

	   })
	   .catch(function(err) {
	   	console.log(err)
	   	  	return function (dispatch) {
			    dispatch(get_usuarios(tipo_usuario ,2));
			}
	   });
}
