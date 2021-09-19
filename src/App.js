import './App.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { Route, Switch, BrowserRouter} from 'react-router-dom';
import Navigation from './navigation/Navigation';
import InventoryManagement from './inventory_management/InventoryManagement';
import ResolveModelFromPart from './resolve_model_from_part/ResolveModelFromPart';
import ReceiveParts from './receive_parts/ReceiveParts'; 
// Main React Component

class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {

    }

  }

  //                         METHODS


  render(){


    return (
      <div className="App">
        <BrowserRouter>
          <Navigation />


          {/* Switch and router will go here  */}

          <Switch>
            <Route path="/" exact component={InventoryManagement} />
            <Route path="/inventoryManagement" exact component={InventoryManagement} />
            <Route path="/resolveModelFromPart" exact component={ResolveModelFromPart} />
            <Route path="/receiveParts" exact component={ReceiveParts} />

         </Switch>
       </BrowserRouter>
      </div>
    );
  }
}

export default App;
