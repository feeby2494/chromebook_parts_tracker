import React,{Component} from 'react';
import jwt_decode from "jwt-decode";
import { Redirect} from 'react-router-dom';
import {withRouter} from 'react-router'; // OM!!! This gives me back history on this.props!!!!!
import Button from 'react-bootstrap/Button';
// import Jumbotron from 'react-bootstrap/Jumbotron';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

class Login extends Component {
    constructor(props){
        super(props);
        this.state={
            username:'',
            password:'',
            message: null
        };
        this.handleInputChange = this.handleInputChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    handleInputChange =(e)=>{
        const {value,name}= e.target;
        this.setState({
            [name]:value,

        });
    }

    onSubmit =(e)=>{
        e.preventDefault();
        let headers = new Headers();
        headers.set('Authorization', 'Basic ' + btoa(this.state.username + ":" + this.state.password));
        fetch(`${process.env.REACT_APP_API_URL}/user/login`,{
            method:'POST',
            body: JSON.stringify(this.state),
            headers: headers,
        })
        .then(res => {
            return res.json();
        })
        .then(data => {
          sessionStorage.setItem('token', data.token);
          sessionStorage.setItem('public_id', jwt_decode(data.token).public_id);
        //   let nextUrl = '/' + jwt_decode(data.token).public_id;
          this.props.history.go(this.props.currentURL);
        }).catch(err => {
            this.setState({
                message: "Error: wrong password or username"
            });
        })


    }
    render(){
        return(
          <div id="login">
            <Row >
              <Col md={2}></Col>
              <Col md={8} className="justify-content-lg-center">
                <div className="jumbotron mr-5 ml-5 mt-5">
                  <Row>
                    <Col>
                      <h1>Login</h1>
                        {(
                            this.state.message && 
                            <p class="text-danger">{this.state.message}</p>
                        )}
                    </Col>
                  </Row>
                  <Row>
                    
                    <Col lg={6} className="">
                      <Form.Group controlId="username-input">
                        <Form.Label for="username-input">Username:</Form.Label>
                        <Form.Control as="input" type="username" autoComplete="true" name="username" placeholder="Enter username" value={this.state.username} onChange={this.handleInputChange}>
                        </Form.Control>
                      </Form.Group>
                    </Col>
                    <Col lg={6} className="">
                      <Form.Group controlId="password-input">
                        <Form.Label for="password-input">Password:</Form.Label>
                        <Form.Control as="input" type="password"  autoComplete="true" name="password" placeholder="Enter password" value={this.state.password} onChange={this.handleInputChange}>
                        </Form.Control>
                      </Form.Group>
                    </Col>
                    
                  </Row>
                  <Row>

                    <Col style={{ display: 'flex', justifyContent: 'flex-end' }}>
                      <Button className="mr-4" onClick={this.onSubmit} type="submit" value="Login" variant="info">Login</Button> {' '}
                    </Col>
                  </Row>
                </div>
              </Col>
              <Col md={2}></Col>
            </Row>
          </div>
            // <form onSubmit={this.onSubmit}>
            //     <h1>Login</h1>
            //     <input type="username" autoComplete="true" name="username" placeholder="Enter username" value={this.state.username} onChange={this.handleInputChange}></input>
            //     <input type="password"  autoComplete="true" name="password" placeholder="Enter password" value={this.state.password} onChange={this.handleInputChange}></input>
            //     <input type="submit" value="Login"/>
            //     <input type="button" value="Register"/>
            //     <p>{this.props.loggedIn}</p>
            // </form>
        )
    }
}

export default withRouter(Login)
