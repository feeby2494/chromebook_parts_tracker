import './App.css';
import React from 'react';
import ReactDOM from 'react-dom';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

// Main React Component

class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      chromebook_parts : {},
      brands: [],
      models: [],
      repairs: [],
      parts: null,
      current_brand : null,
      current_path: '',
      current_model_name : null,
      current_model_number : null,
      current_repair : null,
      current_parts : []
    }
    this.getChromebookJSON = this.getChromebookJSON.bind(this);
    this.setBrands = this.setBrands.bind(this);
    this.setModels = this.setModels.bind(this);
    this.setRepairs = this.setRepairs.bind(this);
    this.setParts = this.setParts.bind(this);
    this.handleBrand = this.handleBrand.bind(this);
    this.handleModelName = this.handleModelName.bind(this);
    this.handleModelNumber = this.handleModelNumber.bind(this);
    this.handleRepair = this.handleRepair.bind(this);
    this.handleParts = this.handleParts.bind(this);
  }

  //                         METHODS
  getChromebookJSON(event) {
    fetch('http://127.0.0.1:5000/api/chromebook_parts', {
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
        // 'Contet-Type': 'application/x-www-form-urlencoded',
      }
    })
    .then(response => response.json())
    .then((data) => {
      this.setState({
        chromebook_parts: data,
        brands: Object.keys(data['brands'])
      });
      console.log(
        Object.keys(data['brands']['dell'])
      )
    });
  }
  componentDidMount(){
    this.getChromebookJSON();
  }
  setBrands(event) {

  }
  setModels(event) {

  }
  setRepairs(event) {

  }
  setParts(event) {

  }
  handleBrand(event){
    this.setState({
      current_brand: event.target.value,
      current_repair: null,
      parts: null,
      current_parts: null,
      current_model_name: null
    }, () => {
      this.setState({
        models: Object.keys(this.state.chromebook_parts['brands'][this.state.current_brand])
      });
    });


  }
  handleModelName(event){
    this.setState({
      current_model_name: event.target.value,
      current_parts: null,
      current_repair: null,
      parts: null
    }, () => {
      this.setState({
        repairs: Object.keys(this.state.chromebook_parts['brands'][this.state.current_brand][this.state.current_model_name])
      })
    });
  }
  handleModelNumber(event){

  }
  handleRepair(event){
    this.setState({
      current_repair: event.target.value,
    }, () => {
      this.setState({
        parts: this.state.chromebook_parts['brands'][this.state.current_brand][this.state.current_model_name][this.state.current_repair]["parts"]
      });
    });
  }
  handleParts(event){
    event.preventDefault();
    this.setState({
      current_parts: this.state.parts
    });
  }

  render(){


    return (
      <div className="App">
        <Container>
          <Row className="mt-5">
            <Col sm={12} align="center">
              <Card>
                <Card.Body>
                  <Form>
                    <Form.Label>Choose a Brand:</Form.Label>
                    <Form.Control as="select" id="select-brand" onChange={this.handleBrand}>
                      <option disabled="disabled" selected="selected">Select a Brand</option>
                      {
                        this.state.brands.map((brand) => {
                          return <option value={brand}>{brand}</option>
                        })
                      }
                    </Form.Control>
                      {this.state.current_brand  ?
                          <div>
                            <Form.Label> Choose Model </Form.Label>
                            <Form.Control as="select" id="select-model" onChange={this.handleModelName}>
                              <option disabled="disabled" selected="selected">Select a Model</option>
                              {
                                this.state.models.map((model) => {
                                  return <option value={model}>{model}</option>
                                })
                              }
                            </Form.Control>
                          </div>
                        :
                          <br />

                      }
                      <br />
                      {
                        this.state.current_model_name ?
                          <div>
                            <Form.Label>Choose Repair Type</Form.Label>
                            <Form.Control as="select" id="select-repair" onChange={this.handleRepair}>
                              <option value="" selected disabled hidden>Choose here</option>
                              {
                                    this.state.repairs.map((repair) => {
                                      return <option value={repair}>{repair}</option>
                                    })
                              }
                            </Form.Control>
                          </div>
                        :
                          <br />
                      }
                      <Button className="mt-2" onClick={this.handleParts}>Find parts for this repair</Button>
                  </Form>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          <Row>
            <Col sm={12} align="center">
              <Card>
                <Card.Body>
                  {
                    this.state.current_parts ?
                      <div>
                        <ListGroup as="ul">
                          <ListGroup.Item as="li" active>Avaibale Parts for this repair</ListGroup.Item>
                          {this.state.current_parts.map((part) => {
                            return <ListGroup.Item as="li">{part}</ListGroup.Item>
                          })}
                        </ListGroup>
                      </div>
                    :
                      <br />
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

export default App;
