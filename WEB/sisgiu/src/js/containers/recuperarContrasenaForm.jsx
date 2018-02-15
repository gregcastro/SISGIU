// Login de la pagina
import { Button, Input, Row, Col, Form, FormGroup, Label, Alert} from 'reactstrap';
import React,{Component} from 'react';
import {recuperarContrasenaMail} from '../actions/recuperarContrasenaMail.jsx';
import {bindActionCreators} from 'redux';
import { connect } from 'react-redux';

//Spinner
import { PulseLoader } from 'halogenium';

class RecuperarContrasenaForm extends Component{      

	constructor(props) {
        super(props);
    	this.state = {
        	cedula: '',
        	loading: false,
    	};

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }


    handleChange(e) {
        const { name, value } = e.target;
        this.setState({ [name]: value });
    }

    handleSubmit(e) {
        e.preventDefault();

        const { cedula } = this.state;
        if (cedula) {
        	this.setState({loading: true})
        	this.props.status['bad_input'] = false;
        	this.props.status['correo_enviado'] = false;
            this.props.recuperarContrasenaMail(cedula);
        }
    }

	render(){
			const { cedula } = this.state;
			return (
					<div >

						<Form onSubmit={this.handleSubmit}>
							<Row>
								<Col lg='4' md='4' sm='3' xs='2'></Col>
								<Col md='4' sm='6' xs='8' className="border border-info border-bottom-0"> 
							        <br/>
							        <h5>Recuperación de contraseña</h5>
									
							    </Col>
							    <Col lg='4' md='4' sm='3' xs='2'></Col> 
							</Row>	

							<Row>					
								<Col lg='4' md='4' sm='3' xs='2'></Col>
								<Col md='4' xs='8' sm='6' className="border border-info border-top-0 border-bottom-0"> 							       
							      	
							      	{this.state.loading && !this.props.status['bad_input'] && !this.props.status['correo_enviado'] &&
							      	
							      		<center><PulseLoader color="#b3b1b0" size="16px" margin="4px"/></center>
							      	}

							      	{this.props.status['bad_input'] &&
	                    		      <Alert color="danger">
								        Cédula errónea
								      </Alert>
                    				}
                    				{this.props.status['correo_enviado'] &&
	                    		      <Alert color="success">
								        Correo enviado satisfactoriamente
								      </Alert>
                    				}

                    				<hr />
							        <FormGroup>
							          <Label for="cedula">Cédula</Label>
							          <Input type="text" name="cedula" id="cedula" value={cedula} required onChange={this.handleChange} placeholder="Ej: 11122233"/> 
							          <font size="1">Se le enviará un correo electronico con un link para poder restablecer su contraseña</font>
							        </FormGroup>
							    </Col>
							    <Col lg='4' md='4' sm='3' xs='2'></Col>
							</Row>
							<Row>
								<Col lg='4' md='4' sm='3' xs='2'></Col>
								<Col md='4' xs='8' sm='6' className="border border-info border-top-0 text-center">
						        	<br />
						        	<Button color="primary">Restablecer</Button>
						        	<br/>
						        	<a href='/login'>Iniciar sesión</a>
						        	<br/><br/>
						      	</Col>
						      	<Col lg='4' md='4' sm='3' xs='2'></Col>
							</Row>

							
					    </Form>

					</div>
				)
		}
}

const mapStateToProps = (state)=> {
	return{
		status: state.recuperarContrasena
	};
}

const mapDispatchToProps = (dispatch) => {
	return bindActionCreators({recuperarContrasenaMail: recuperarContrasenaMail}, dispatch )
}

export default connect(mapStateToProps, mapDispatchToProps)(RecuperarContrasenaForm);