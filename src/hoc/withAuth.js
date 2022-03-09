import React,{Component} from 'react';
import jwt_decode from "jwt-decode";
import {Redirect} from 'react-router-dom';
import Login from '../login/Login';

const withAuth = (ComponentInside) => {
 return class extends Component {
    constructor(){
        super();
        this.state={
            loading:true,
            redirect:false,
            currentPublicId: sessionStorage.getItem('public_id')
        };
    }

    componentDidMount() {
      const myHeaders = new Headers();

      myHeaders.append('Content-Type', 'application/json');
      myHeaders.append('Authorization', `Bearer ${sessionStorage.getItem('token')}`);
      myHeaders.append('x-access-token', sessionStorage.getItem('token'));

        fetch(`${process.env.REACT_APP_API_URL}/user/${this.state.currentPublicId}`, {
            credentials: "include",
            headers: myHeaders

        })
          .then(res => {
            if (res.status === 200) {
              this.setState({ loading: false });
            } else {
              const error = new Error(res.error);
              throw error;
            }
          })
          .catch(err => {
            console.error(err);
            this.setState({ loading: false, redirect: true });
          });
      }


    render(){
        const{loading, redirect} = this.state;
        if(loading){
            return null;
        }
        if(redirect){
            console.log(window.location.pathname)
            if(!this.state.currentPublicId){
                return <Login currentURL={window.location.pathname}/>
            }
            
        }
        return <ComponentInside {...this.props}/>
    }
}
}


export default withAuth;
