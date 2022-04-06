import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';
import SupplyInventoryMgt from './components/SupplyInventoryMgt';
import LookUpAllSupplyItems from './components/LookUpAllSupplyItems';
import LookUpSupplyItemInventory from './components/LookUpSupplyItemInventory';
import LookUpInventoryByRoom from './components/LookUpInventoryByRoom';

// Main React Component

class OfficeSupplies extends React.Component {
  constructor(props){
    super(props);
    this.state = {
        vendors : null,
        currentVendor : null,
        brands: null,
        currentBrand: null,
        supplyName: null,
        currentSupplyName: null,
        supplyItems: null,
        currentSupplyItem: null,
        supplySKU: null,
        currentSupplySKU: null,
        supplyInventory: null,
        currentSupplyInventory: null,
        locationCode: null,
        locationBin: null,
        locationShelf: null,
        locationRoom: null,
        currentLocationCode: null,
        currentLocationBin: null,
        currentLocationShelf: null,
        currentLocationRoom: null,
        supplyInventoryCountInBin: null,
        currentInventoryCountInBin: null
    }
    this.handleInput = this.handleInput.bind(this);
    
  }

  handleInput(event) {
      if( this.state.hasOwnProperty(`${event.target.id}`)) {
        // let tabName = `${event.target.id}`;
        this.setState({
          [`${event.target.id}`]: event.target.value
        });
      }
  }

 

  render () {
    return (
      <div className="resolvePartToModel">
        <Container>
          
          <Row>
            <p value="I'm a office supply inventory app."/>
          </Row>
          <SupplyInventoryMgt />

        </Container>
      </div>
    );
  }
}

export default OfficeSupplies;
