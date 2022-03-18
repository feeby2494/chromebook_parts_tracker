import './App.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Switch, BrowserRouter} from 'react-router-dom';
import withAuth from './hoc/withAuth';
import Login from './login/Login';
import Navigation from './navigation/Navigation';
import InventoryManagement from './inventory_management/InventoryManagement';
import ResolveModelFromPart from './resolve_model_from_part/ResolveModelFromPart';
import ReceiveParts from './receive_parts/ReceiveParts'; 
import Register from './register/Register';
import useToken from './useToken';
// Main React Component

const App= (props) => {
  // const { token, setToken } = useToken();

  // if(!token) {
  //   return <Login setToken={setToken} />
  // }

  

  return (
    <div className="App">
      <BrowserRouter>
        <Navigation />


        {/* Switch and router will go here  */}
        
        <Switch>
          <Route path="/" exact component={withAuth(InventoryManagement)} />
          <Route path="/login" >
            <Login  history={props.history}/>
          </Route>
          <Route path="/inventoryManagement" exact component={withAuth(InventoryManagement)} />
          <Route path="/resolveModelFromPart" exact component={withAuth(ResolveModelFromPart)} />
          <Route path="/receiveParts" exact component={withAuth(ReceiveParts)} />
          <Route path="/register"> 
            <Register history={props.history}/>
          </Route>

        </Switch>
      </BrowserRouter>
    </div>
  );
  
}

export default App;