// Dependencies
import React, {Component} from 'react';
import {NavItem, NavLink, Nav } from 'reactstrap';
import { connect } from 'react-redux';

class NavBarAdministrativo extends Component{

  render() {
    
      return (
        <Nav navbar >
                                
          <NavItem>
            <NavLink href="/inicio" disabled={!this.props.activeUser.cargado}>Inicio</NavLink>
          </NavItem>

          <NavItem>
              <NavLink href="/estudiantes" disabled={!this.props.activeUser.cargado}>Estudiantes</NavLink>
          </NavItem>

          <NavItem>
            <NavLink href="/historial" disabled={!this.props.activeUser.cargado}>Historial Académico</NavLink>
          </NavItem>

          <NavItem>
            <NavLink href="/programacionAcademica" disabled={!this.props.activeUser.cargado}>Programación Académica</NavLink>
          </NavItem>



        </Nav>

      )

  }

}



const mapStateToProps = (state)=> {
  return{
    activeUser: state.activeUser,
  };
}



export default connect(mapStateToProps)(NavBarAdministrativo);
