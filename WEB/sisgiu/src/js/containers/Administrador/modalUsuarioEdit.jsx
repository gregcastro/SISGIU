import React from 'react';
import { Input, Form, FormGroup, Label, Row, Col, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import FontAwesomeIcon from 'react-fontawesome';
import '../../../css/moduloUsuarioAdministrador.css';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { host } from '../../components/globalVariables';

// Components
import { editarUsuario, editarDocumento } from '../../actions/moduloUsuarioAdministrador';

class ModalUsuarioEdit extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      modal: false,
      usuario: {
        tipo_documento: this.props.usuario['tipo_documento'],
        cedula: this.props.usuario['cedula'],
        first_name: this.props.usuario['first_name'],
        segundo_nombre: this.props.usuario['segundo_nombre'],
        last_name: this.props.usuario['last_name'],
        segundo_apellido: this.props.usuario['segundo_apellido'],
        email: this.props.usuario['email'],
        celular: this.props.usuario['celular'],
        telefono_casa: this.props.usuario['telefono_casa'],
        telefono_trabajo: this.props.usuario['telefono_trabajo'],
        nacionalidad: this.props.usuario['nacionalidad'],
        sexo: this.props.usuario['sexo'],
        estado_civil: this.props.usuario['estado_civil'],
        foto: this.props.usuario['foto'],
        fecha_nacimiento: this.props.usuario['fecha_nacimiento'],
        password: this.props.usuario['password']
      },
      direccion: this.props.usuario['direccion'],
      rif: this.props.usuario['rif'],
      curriculum: this.props.usuario['curriculum'],
      permiso_ingresos: this.props.usuario['permiso_ingresos'],
      coordinador: this.props.usuario['coordinador'],
      tipo_postgrado: this.props.usuario['tipo_postgrado'],
      id_tipo_postgrado: this.props.usuario['id_tipo_postgrado'],
      id_estado_estudiante: this.props.usuario['id_estado_estudiante'],
      estado_estudiante: this.props.usuario['estado_estudiante'],
      rif_file: undefined,
      curriculum_file: undefined,
      permiso_ingresos_file: undefined,
      visible: true,
      is_disabled: this.props.is_disabled,
    };
    this.toggle = this.toggle.bind(this);
    this.handleChangeUsuario = this.handleChangeUsuario.bind(this);
    this.handleChangeExtraData = this.handleChangeExtraData.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.subirDocumento = this.subirDocumento.bind(this);
    this.handleChangeDocumento = this.handleChangeDocumento.bind(this);
    this.handleChangeCheckbox = this.handleChangeCheckbox.bind(this);
    this.get_today = this.get_today.bind(this);

  }

  toggle() {
    this.setState({
      modal: !this.state.modal
    });
    if (!this.state.modal) { this.props.onDismiss(); };
  }

  componentWillReceiveProps(props) {
    this.setState({ "direccion": props.usuario.direccion });
    this.setState({ "usuario": props.usuario });
    this.setState({ "rif": props.usuario.rif });
    this.setState({ "curriculum": props.usuario.curriculum });
    this.setState({ "permiso_ingresos": props.usuario.permiso_ingresos });
    this.setState({ "coordinador": props.usuario.coordinador });
    this.setState({ "tipo_postgrado": props.usuario.tipo_postgrado });
    this.setState({ "id_tipo_postgrado": props.usuario.id_tipo_postgrado });
    this.setState({ "id_estado_estudiante": props.usuario.id_estado_estudiante });
  }

  handleChangeUsuario(e) {
    const { name, value } = e.target;
    var usuario = this.state.usuario;
    usuario[name] = value;
    this.setState({ usuario })

  }

  handleChangeDocumento(e) {
    let name = e.target.name + '_file';
    this.setState({ [name]: e.target.files[0] })
  }

  handleChangeExtraData(e) {
    const { name, value } = e.target;
    this.setState({ [name]: value });
  }

  handleChangeCheckbox(e) {
    const { name, checked } = e.target;
    this.setState({ [name]: checked });
  }

  handleSubmit(e) {
    e.preventDefault();
    this.props.triggerParentUpdate();
    this.props.editarUsuario(this.state, this.props.usuario, this.props.tipo_usuario);
    this.props.triggerParentUpdate();
    this.toggle();
  }

  subirDocumento(tipo_documento) {
    let documento;
    switch (tipo_documento) {

      case 'rif':
        documento = this.state.rif_file
        break;

      case 'curriculum':
        documento = this.state.curriculum_file
        break;

      case 'permiso_ingresos':
        documento = this.state.permiso_ingresos_file
        break;

      default:
        break;
    }
    if (documento) {
      let extension = documento.name.split('.')[1];
      let size = documento.size;
      if ((extension === "pdf" || extension === "doc" || extension === "docx") && size <= 52428800) {
        this.props.triggerParentUpdate();
        this.props.editarDocumento(tipo_documento, documento, this.state.usuario.cedula);
        this.props.triggerParentUpdate();
        this.toggle();
      } else {
        alert('El archivo debe ser doc, docx o pdf. Además no debe superar los 50 MB');
      }
    } else {
      alert('No ha subido ningún archivo');
    }
  }


  get_today() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();
    if (dd < 10) {
      dd = '0' + dd
    }
    if (mm < 10) {
      mm = '0' + mm
    }

    today = yyyy + '-' + mm + '-' + dd;
    return today;
  }

  render() {
    let listPostgrados = '';
    let lista_estadoEstudiante = '';

    if (this.props.adminUser.lista_postgrados && this.props.adminUser.lista_postgrados.length > 0) {
      listPostgrados = this.props.adminUser.lista_postgrados.map((tipo_postgrado) =>
        <option key={tipo_postgrado['id']} value={tipo_postgrado['id']} name={tipo_postgrado['tipo']}> {tipo_postgrado['tipo']} </option>
      );
    }

    if (this.props.adminUser.lista_estadoEstudiante && this.props.adminUser.lista_estadoEstudiante.length > 0) {
      lista_estadoEstudiante = this.props.adminUser.lista_estadoEstudiante.map((estado_estudiante) =>
        <option key={estado_estudiante['id']} value={estado_estudiante['id']} name={estado_estudiante['estado']}> {estado_estudiante['estado']} </option>
      );
    }

    return (
      <div>
        {!this.state.is_disabled ?
          <Button color="success" size='sm' onClick={this.toggle} data-toggle="tooltip" title="Editar"><FontAwesomeIcon name="edit" /></Button>
          :
          <Button color="info" size='sm' onClick={this.toggle} data-toggle="tooltip" title="Ver">Ver información personal</Button>
        }
        <Modal isOpen={this.state.modal} toggle={this.toggle} className={this.props.className}>
          {!this.state.is_disabled ?
            <ModalHeader toggle={this.toggle}>
              Editar usuario
            </ModalHeader>
            :
            <ModalHeader toggle={this.toggle}>
              Ver usuario
            </ModalHeader>
          }
          <Form id="Form1" onSubmit={this.handleSubmit}>
            <ModalBody>
              <img className="center-img" width="100px" height="100px" src={this.state.usuario['foto']} alt="foto_usuario" />
              <br />
              <div>
                <br />
                <Row>
                  <Col sm="12">
                    <FormGroup row>
                      <Label for="identificacion" sm={4}>Cédula o Pasaporte</Label>
                      <Col sm={8}>
                        <Input bsSize="sm" type="text" name="cedula" id="identificacion" defaultValue={this.state.usuario['cedula']} readOnly required />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label className="required" for="first_name" sm={4}>Primer Nombre</Label>
                      <Col sm={8}>
                        <Input maxLength={50} bsSize="sm" disabled={this.state.is_disabled} type="text" name="first_name" id="first_name" onChange={this.handleChangeUsuario} defaultValue={this.state.usuario['first_name']} required />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label for="segundo_nombre" sm={4}>Segundo Nombre</Label>
                      <Col sm={8}>
                        <Input maxLength={50} bsSize="sm" disabled={this.state.is_disabled} type="text" name="segundo_nombre" id="segundo_nombre" onChange={this.handleChangeUsuario} defaultValue={this.state.usuario['segundo_nombre']} />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label className="required" for="last_name" sm={4}>Primer Apellido</Label>
                      <Col sm={8}>
                        <Input maxLength={50} bsSize="sm" disabled={this.state.is_disabled} type="text" name="last_name" id="last_name" onChange={this.handleChangeUsuario} defaultValue={this.state.usuario['last_name']} required />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label className="required" for="segundo_apellido" sm={4}>Segundo Apellido</Label>
                      <Col sm={8}>
                        <Input maxLength={50} bsSize="sm" disabled={this.state.is_disabled} type="text" name="segundo_apellido" id="segundo_apellido" onChange={this.handleChangeUsuario} defaultValue={this.state.usuario['segundo_apellido']} required />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label for="fecha_nacimiento" sm={4}>Nacimiento</Label>
                      <Col sm={8}>
                        <Input max={this.get_today()} min="1930-01-01" bsSize="sm" disabled={this.state.is_disabled} type="date" name="fecha_nacimiento" id="fecha_nacimiento" onChange={this.handleChangeUsuario} readOnly defaultValue={this.state.usuario['fecha_nacimiento']} required />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label className="required" for="email" sm={4}>Correo</Label>
                      <Col sm={8}>
                        <Input bsSize="sm" disabled={this.state.is_disabled} type="email" name="email" id="email" onChange={this.handleChangeUsuario} value={this.state.usuario['email']} required />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label for="Celular" sm={4}>Celular</Label>
                      <Col sm={8}>
                        <Input min={1000000000} max={999999999999} bsSize="sm" disabled={this.state.is_disabled} type="number" name="celular" id="celular" onChange={this.handleChangeUsuario} value={this.state.usuario['celular']} />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label for="telefono_casa" sm={4}>Tlf. Casa</Label>
                      <Col sm={8}>
                        <Input min={1000000000} max={999999999999} bsSize="sm" disabled={this.state.is_disabled} type="number" name="telefono_casa" id="telefono_casa" onChange={this.handleChangeUsuario} value={this.state.usuario['telefono_casa']} />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label for="telefono_trabajo" sm={4}>Tlf. Trabajo</Label>
                      <Col sm={8}>
                        <Input min={1000000000} max={999999999999} bsSize="sm" disabled={this.state.is_disabled} type="number" name="telefono_trabajo" id="telefono_trabajo" onChange={this.handleChangeUsuario} value={this.state.usuario['telefono_trabajo']} />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label className="required" for="nacionalidad" sm={4}>Nacionalidad</Label>
                      <Col sm={8}>
                        <Input bsSize="sm" disabled={this.state.is_disabled} type="text" name="nacionalidad" id="nacionalidad" onChange={this.handleChangeUsuario} value={this.state.usuario['nacionalidad']} required />
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label className="required" for="sexo" sm={4}>Sexo</Label>
                      <Col sm={8}>
                        <Input bsSize="sm" value={this.state.value} disabled={this.state.is_disabled} defaultValue={this.state.usuario['sexo']} onChange={this.handleChangeUsuario} type="select" name="sexo" id="sexo" required>
                          <option value="M" name="M">M</option>
                          <option value="F" name="F">F</option>
                        </Input>
                      </Col>
                    </FormGroup>
                    <FormGroup row>
                      <Label className="required" for="estado_civil" sm={4}>Estado Civil</Label>
                      <Col sm={8}>
                        <Input bsSize="sm" disabled={this.state.is_disabled} value={this.state.value} defaultValue={this.state.usuario['estado_civil']} onChange={this.handleChangeUsuario} type="select" name="estado_civil" id="estado_civil" required>
                          <option value="Soltero" name="Soltero">Soltero</option>
                          <option value="Casado" name="Casado">Casado</option>
                          <option value="Viudo" name="Viudo">Viudo</option>
                          <option value="Divorciado" name="Divorciado">Divorciado</option>
                        </Input>
                      </Col>
                    </FormGroup>

                    {this.props.tipo_usuario === 'estudiantes' &&
                      <div>
                        <FormGroup row>
                          <Label for="direccion" sm={4}>Dirección</Label>
                          <Col sm={8}>
                            <Input bsSize="sm" disabled={this.state.is_disabled} type="textarea" name="direccion" id="direccion" onChange={this.handleChangeExtraData} value={this.state.direccion} />
                          </Col>
                        </FormGroup>
                        {!this.state.is_disabled ?
                          <div>
                            <FormGroup row>
                              <Label className="required" for="id_tipo_postgrado" sm={4}>Postgrado</Label>
                              <Col sm={8}>
                                <Input bsSize="sm" disabled={this.state.is_disabled} value={this.state.value} defaultValue={this.state['id_tipo_postgrado']} onChange={this.handleChangeExtraData} type="select" name="id_tipo_postgrado" id="id_tipo_postgrado" required>
                                  {listPostgrados}
                                </Input>
                              </Col>
                            </FormGroup>

                            <FormGroup row>
                              <Label className="required" for="estado_estudiante" sm={4}>Estado</Label>
                              <Col sm={8}>
                                <Input bsSize="sm" disabled={this.state.is_disabled} value={this.state.value} defaultValue={this.state['id_estado_estudiante']} onChange={this.handleChangeExtraData} type="select" name="id_estado_estudiante" id="id_estado_estudiante" required>
                                  {lista_estadoEstudiante}
                                </Input>
                              </Col>
                            </FormGroup>
                          </div>
                          :
                          <div>
                            <FormGroup row>
                              <Label className="required" for="id_tipo_postgrado" sm={4}>Postgrado</Label>
                              <Col sm={8}>
                                <Input bsSize="sm" disabled={this.state.is_disabled} defaultValue={this.state['tipo_postgrado']} type="text" required>
                                </Input>
                              </Col>
                            </FormGroup>

                            <FormGroup row>
                              <Label className="required" for="estado_estudiante" sm={4}>Estado</Label>
                              <Col sm={8}>
                                <Input bsSize="sm" disabled={this.state.is_disabled} defaultValue={this.state['estado_estudiante']} type="text" required>
                                </Input>
                              </Col>
                            </FormGroup>
                          </div>
                        }
                      </div>
                    }

                    {this.props.tipo_usuario === 'docentes' &&
                      <div>
                        <FormGroup row>
                          <Label for="direccion" sm={4}>Dirección</Label>
                          <Col sm={8}>
                            <Input bsSize="sm" disabled={this.state.is_disabled} type="textarea" name="direccion" id="direccion" onChange={this.handleChangeExtraData} value={this.state.direccion} />
                          </Col>
                        </FormGroup>
                        <FormGroup row>
                          <Label for="rif" sm={3}>RIF</Label>
                          <Col sm={5}>
                            <Input className="form-control" disabled={this.state.is_disabled} bsSize="sm" type="file" name="rif" id="rif" onChange={this.handleChangeDocumento} />
                          </Col>
                          <Col sm={2}>
                            {this.state.rif !== host + 'media/' ?
                              <a href={this.state.rif} target='_blank' ><Button color="primary" size='sm' type='button'> Descargar </Button> </a>
                              :
                              <a href={this.state.rif} target='_blank' ><Button disabled color="primary" size='sm' type='button'> Descargar </Button> </a>
                            }
                          </Col>
                          <Col sm={2}>
                            <Button disabled={this.state.is_disabled} onClick={() => { this.subirDocumento('rif') }} color="primary" size='sm'> Subir </Button>
                          </Col>
                        </FormGroup>

                        <FormGroup row>
                          <Label for="curriculum" sm={3}>Curriculum</Label>
                          <Col sm={5}>
                            <Input disabled={this.state.is_disabled} className="form-control" bsSize="sm" type="file" name="curriculum" id="curriculum" onChange={this.handleChangeDocumento} />
                          </Col>
                          <Col sm={2}>
                            {this.state.curriculum !== host + 'media/' ?
                              <a href={this.state.curriculum} target='_blank'><Button color="primary" size='sm' type='button'> Descargar </Button> </a>
                              :
                              <a href={this.state.curriculum} target='_blank'><Button disabled color="primary" size='sm' type='button'> Descargar </Button> </a>
                            }
                          </Col>
                          <Col sm={2}>
                            <Button disabled={this.state.is_disabled} onClick={() => { this.subirDocumento('curriculum') }} color="primary" size='sm'> Subir </Button>
                          </Col>
                        </FormGroup>

                        <FormGroup row>
                          <Label for="permiso_ingresos" sm={3}>Permisos</Label>
                          <Col sm={5}>
                            <Input disabled={this.state.is_disabled} className="form-control" bsSize="sm" type="file" name="permiso_ingresos" id="permiso_ingresos" onChange={this.handleChangeDocumento} />
                          </Col>
                          <Col sm={2}>
                            {this.state.permiso_ingresos !== host + 'media/' ?
                              <a href={this.state.permiso_ingresos} target='_blank'><Button color="primary" size='sm' type='button'> Descargar </Button> </a>
                              :
                              <a href={this.state.permiso_ingresos} target='_blank'><Button disabled color="primary" size='sm' type='button'> Descargar </Button> </a>
                            }
                          </Col>
                          <Col sm={2}>
                            <Button disabled={this.state.is_disabled} onClick={() => { this.subirDocumento('permiso_ingresos') }} color="primary" size='sm'> Subir </Button>
                          </Col>
                        </FormGroup>

                        <FormGroup check>
                          <Label check>
                            <Input disabled={this.state.is_disabled} bsSize="sm" defaultChecked={this.state.coordinador} type="checkbox" name="coordinador" id="coordinador" onChange={this.handleChangeCheckbox} />{' '}
                            Es coordinador
                                </Label>
                        </FormGroup>

                        {this.state.coordinador &&
                          <FormGroup row>
                            <Label className="required" for="id_tipo_postgrado" sm={4}>Postgrado</Label>
                            <Col sm={8}>
                              <Input bsSize="sm" defaultValue={this.state['id_tipo_postgrado']} onChange={this.handleChangeExtraData} type="select" name="id_tipo_postgrado" id="id_tipo_postgrado" required>
                                <option value={null} name={-1}> {' '} </option>
                                {listPostgrados}
                              </Input>
                            </Col>
                          </FormGroup>
                        }

                      </div>
                    }
                    <font size="2"><span className="required"></span> Campo requerido</font>
                  </Col>
                </Row>

              </div>

            </ModalBody>
            {!this.state.is_disabled &&
              <ModalFooter>
                <Button disabled={this.state.is_disabled} color="success" type="submit">Guardar</Button>{' '}
                <Button disabled={this.state.is_disabled} color="secondary" onClick={this.toggle}>Salir</Button>
              </ModalFooter>
            }
          </Form>
        </Modal>

      </div>
    );

  }
}

const mapStateToProps = (state) => {
  return {
    adminUser: state.adminUser,
  };
}

const mapDispatchToProps = (dispatch) => {
  return bindActionCreators({
    editarUsuario: editarUsuario,
    editarDocumento: editarDocumento,
  },
    dispatch
  )
}

export default connect(mapStateToProps, mapDispatchToProps)(ModalUsuarioEdit);

