import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

// Main React Component

class ReceiveParts extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      partNumber : '',
      partInfo: '',
      partCount : '',
      partLocation: '',
      partAdded: ''
    }
    this.handlePartInput = this.handlePartInput.bind(this);
    this.submitPartInventory = this.submitPartInventory.bind(this);
  }

  handlePartInput(event) {
      if( this.state.hasOwnProperty(`${event.target.id}`)) {
        // let tabName = `${event.target.id}`;
        this.setState({
          [`${event.target.id}`]: event.target.value
        });
      }
  }

  submitPartInventory() {

    fetch(`${process.env.REACT_APP_API_URL}/receive_parts/${this.state.partNumber}`, {
      mode: 'cors',
      method: "POST",
      body: JSON.stringify(
        {
          "count" : this.state.partCount,
          "location_desc" : this.state.partLocation,
          "part_info" : this.state.partInfo
        }
      ),
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      this.setState({
        partAdded: data.parts,
        inventory: data.current_inventory
      })
    })
    .catch(err => console.log(err));
  }

  render () {
    return (
      <div className="resolvePartToModel">
        <Container>
          <Row className="mt-5">
            <Col sm={12} align="center">
              <Card>
                <Card.Header><h2>Part Number to Receive : </h2></Card.Header>

                <Card.Body>
                  <Form>
                    <Form.Label> Enter Part Number (Not the AGID!) :  </Form.Label>
                    <Form.Control as="input" id="partNumber" onChange={this.handlePartInput}>

                    </Form.Control>
                    <Form.Label> Enter Part Info (This is used to differentiate between parts for differnet versions of a model. For example, Intel, MTK, or AMD versions of the same model.) :  </Form.Label>
                    <Form.Control as="input" id="partInfo" onChange={this.handlePartInput}>

                    </Form.Control>
                    <Form.Label> Enter Part Count :  </Form.Label>
                    <Form.Control as="input" id="partCount" onChange={this.handlePartInput}>

                    </Form.Control>
                    <Form.Label> Enter Part Location :  </Form.Label>
                    <Form.Control as="input" id="partLocation" onChange={this.handlePartInput}>

                    </Form.Control>

                    <Button className="mt-3" onClick={this.submitPartInventory} variant="success">Submit Part</Button>
                  </Form>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          <Row className="mt-5">
            <Col sm={12} align="center">
              <Card>
                <Card.Header><h2>Model : </h2></Card.Header>
                <Card.Body>
                  <h3>{this.state.resolvedModel}</h3>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default ReceiveParts;
