import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

// Main React Component

class ResolveModelFromPart extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      partInput : '',
      resolvedRepairs: null,
      message: null
    }
    this.handlePartInput = this.handlePartInput.bind(this);
    this.resolveToModel = this.resolveToModel.bind(this);
  }

  handlePartInput(event) {
    this.setState({
      partInput : event.target.value.trim()
    });
  }

  resolveToModel() {

    fetch(`${process.env.REACT_APP_API_URL}/resolve_model_from_part_number/${encodeURIComponent(this.state.partInput)}`, {
      mode: 'cors',
      method: "GET",
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      this.setState({
        resolvedRepairs: data.repairs
      })
    })
    .catch(err => {
      console.log(err)
      this.state.setState({
        error: `Error: ${err}` 
      });
    });
  }

  render () {
    return (
      <div className="resolvePartToModel">
        <Container>
          <Row className="mt-5">
            <Col sm={12} align="center">
              <Card>
                <Card.Header><h2>Part Number to Resolve : </h2></Card.Header>
                <Card.Body>
                  <Form>
                    <Form.Label> Enter Part Number (Not the AGID!) :  </Form.Label>
                    <Form.Control as="input" id="input-part-number" onChange={this.handlePartInput}>

                    </Form.Control>
                    <Button className="mt-3" onClick={this.resolveToModel} variant="success">Resolve To Repair</Button>
                  </Form>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          <Row className="mt-5">
            <Col sm={12} align="center">
              <Card>
                <Card.Header><h2>Repair Types Associated with this Part Number : </h2></Card.Header>
                <Card.Body>
                  { this.state.resolvedRepairs &&
                    
                    this.state.resolvedRepairs.map((repair) => {
                      return (<h3>{repair.name}</h3>);
                    })
                  }
                  
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default ResolveModelFromPart;
