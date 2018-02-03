// Dependencies
import React, {Component} from 'react';
import { connect } from 'react-redux';
import {Collapse, Navbar, NavbarToggler} from 'reactstrap';

// Components
import NavBarInicio from '../components/navBarInicio';
import NavBarEstudiante from '../components/navBarEstudiante';
import NavBarDocente from '../components/navBarDocente';
import NavBarAdministrativo from '../components/navBarAdministrativo';
import NavBarAdministrador from '../components/navBarAdministrador';

class NavigationBar extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      isOpen: false
    };
  }
  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }

  logout() {
    localStorage.removeItem('user_token');
    // DEBERIA CAMBIAR ESTO POR ALGO RELACIONADO A REACT-ROUTER-DOM
    window.location.reload();
  }

  render() {


    let navigationBar;
    if (this.props.token['loggedIn']) {

      let modulo = this.props.token['modulo'];

      switch ( modulo ) {

        case 'estudiantes':
          navigationBar = ( <NavBarEstudiante /> )
        break;

        case 'docentes':
          navigationBar = ( <NavBarDocente /> )
        break;

        case 'administrativos':
          navigationBar = ( <NavBarAdministrativo /> )
        break;

        case 'usuarios':
          navigationBar = ( <NavBarAdministrador /> )
        break;

        default:
          console.log('jdknawk');
        break;

      }
    } else {
      navigationBar = ( <NavBarInicio /> )
    }



    return (
      <div>
        <Navbar color="faded" light expand="md">
          
          {/*
          <NavbarBrand href="/">
            SISGIU
          </NavbarBrand>
          */}
          <NavbarToggler onClick={this.toggle} />
          <Collapse isOpen={this.state.isOpen} navbar>           
                
               
            { navigationBar }

            {/* !this.props.token['loggedIn'] ? 
              <NavItem>
                <NavLink onClick={this.logout} href='#' >Logout</NavLink>
              </NavItem>
              : ''
            */}

          </Collapse>
        </Navbar>
      </div>
    );
  }
}

const mapStateToProps = (state)=> {
  return{
    token: state.activeUser
  };
}


export default connect(mapStateToProps)(NavigationBar);