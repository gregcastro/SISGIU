// Dependencies
import React, {Component} from 'react';
import { connect } from 'react-redux';
import {bindActionCreators} from 'redux';
import { Alert, Button, Row, Col, ListGroup, ListGroupItem, ListGroupItemHeading, ListGroupItemText} from 'reactstrap';
import { PulseLoader } from 'halogenium';
import Inscripcion from './inscripcion';

// Components
import { get_information, get_periodo_estudiante, get_periodos_tipo_postgrado } from '../../actions/inicio';

class InicioEstudiante extends Component{

  constructor(props) {
      super(props);
      this.state = {
        inscribiendo: false,
        visible: true,
      }
      this.onDismiss = this.onDismiss.bind(this);
      this.props.get_information(this.props.token['user']);
      this.props.get_periodos_tipo_postgrado("en inscripcion", this.props.token['user'].id_tipo_postgrado);
      this.props.get_periodo_estudiante(this.props.token['user'].usuario.cedula, "en inscripcion");

      this.get_ListItems = this.get_ListItems.bind(this);
  }

  onDismiss() {
    this.setState({ visible: false });
  }

  get_ListItems(dias) {
    var listItems = "";
    if(this.props.estudianteUser['materias'] && this.props.estudianteUser['materias'].length > 0){
      listItems = this.props.estudianteUser['materias'].map((valor, index) =>{
        var lista_docentes = [];
        for (var i = 0; i < valor['docente']['horario_dia'].length; i++) {

            lista_docentes[i] = <font key={i}> {dias[valor['docente']['horario_dia'][i]]} {valor['docente']['horario_hora'][i]} <br /></font>
        }
        return (
          <ListGroupItem key={index}>
            <ListGroupItemHeading>({valor['codigo']}) {valor['nombre']}</ListGroupItemHeading>
            <ListGroupItemText key={valor['codigo']}>
                {lista_docentes}
                Prof: {valor['docente']['first_name']} {valor['docente']['last_name']}
                
            </ListGroupItemText>
        </ListGroupItem>
        )
      });
    }else{
      if(this.props.estudianteUser['tiene_asignaturas']){
        listItems = <center><PulseLoader color="#b3b1b0" size="16px" margin="4px"/></center>
      }
    }

    return listItems;
  }

  enInscripcion(){
    this.setState({inscribiendo: !this.state.inscribiendo});
  }

  render(){
    const dias = {
      "0":"Lunes",
      "1":"Martes",
      "2":"Miercoles",
      "3":"Jueves",
      "4":"Viernes",
      "5":"Sabado",
      "6":"Domingo",
    }

      if(!this.state.inscribiendo){
        return(
            <div>
            {/*ALERT DE ERROR*/}
            {this.props.estudianteUser['error_inscripcion'] &&
              <Col md='12' className="text-center">
                <Alert color="danger" isOpen={this.state.visible} toggle={this.onDismiss}>
                  Ha ocurrido un error en el proceso de inscripción
                </Alert>
              </Col>
            }

            {/*ALERT DE EXITO*/}
            {this.props.estudianteUser['inscripcion_exitosa'] &&
              <Alert color="success" isOpen={this.state.visible} toggle={this.onDismiss}>
                  Inscripción realizada exitosamente.
              </Alert> 
            }

            <br />
            {!this.props.estudianteUser['inscripcion_exitosa'] && this.props.estudianteUser.first_render && this.props.estudianteUser.lista_periodo_estudiante.length === 0 && this.props.estudianteUser.lista_periodos.length > 0 &&
              <Row>
                <Col md='12' className="text-center">
                  <Button onClick={() => this.enInscripcion()} color="primary">
                    Inscribirse
                  </Button>
                </Col>
              </Row>
            }
              <br />
              <br />
              {!this.props.estudianteUser['tiene_asignaturas'] &&
                <Row>
                   <Col md='12' className="text-center">
                      <h5>Usted no se encuentra inscrito en el periodo actual.</h5>
                  </Col>
                </Row>
              }
              {this.props.estudianteUser['tiene_asignaturas'] &&
                <div>
                  <Row>
                   <Col md='12' className="text-center">
                      <h5>Asignaturas Inscritas</h5>
                  </Col>
                  </Row>
                  <br />
                  <Row>
                    <Col md='12'>
                      <ListGroup>
                        {this.get_ListItems(dias)}
                      </ListGroup>
                    </Col>
                  </Row>
                </div>
              }
            </div>
        );
      } else{
        return (
          <Inscripcion triggerInscripcion={()=> this.enInscripcion() }/>
        );
      }
  }
}


const mapStateToProps = (state)=> {
  return{
    token: state.activeUser,
    estudianteUser: state.estudianteUser
  };
}

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({
    get_information: get_information,
    get_periodo_estudiante: get_periodo_estudiante,
    get_periodos_tipo_postgrado: get_periodos_tipo_postgrado
  }, dispatch )
}


export default connect(mapStateToProps, mapDispatchToProps)(InicioEstudiante);


