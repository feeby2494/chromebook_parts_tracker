import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';

// Main React Component

class ReceiveParts extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      partNumber : '',
      partInfo: '',
      partCount : '',
      partLocation: '',
      partAdded: '',
      selectedFile: null,
      errorPartInput: null
    }
    this.handlePartInput = this.handlePartInput.bind(this);
    this.submitPartInventory = this.submitPartInventory.bind(this);
    this.onFileChange = this.onFileChange.bind(this);
    this.onFileUpload = this.onFileUpload.bind(this);
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

    fetch(`${process.env.REACT_APP_API_URL}/receive_parts/${encodeURIComponent(this.state.partNumber)}`, {
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
    .catch(err => {
      console.log(err)
      this.setState({
        errorPartInput: `Error: ${err}`
      });
    });
  }

  onFileChange(event) {
    this.setState({
      selectedFile: event.target.files[0]
    });
  }

  onFileUpload(event) {

    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    formData.append(
      "myFile",
      this.state.selectedFile,
      this.state.selectedFile.name
    );

    // Details of the uploaded file
    console.log(this.state.selectedFile);

    // Request made to the backend api
    // Send formData object
    fetch(`${process.env.REACT_APP_API_URL}/uploadInventory`, {
      method: 'POST',
      body: formData
    })
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

                    <Form.Row className="align-items-center" className="g-2">
                      <Col lg>
                        <Form.Group className="" controlId="formPartNumber">
                          <InputGroup className="mb-2">
                            <InputGroup.Prepend>
                              <Button variant="outline-primary">Check!</Button>
                            </InputGroup.Prepend>
                            <FormControl id="partNumber" onChange={this.handlePartInput} placeholder="Part Number" />
                          </InputGroup>
                        </Form.Group>
                      </Col>
                      <Col lg>
                        <Form.Group className="" controlId="formPartInfo">
                          <InputGroup className="mb-2">
                            <InputGroup.Prepend>
                              <InputGroup.Text>Part Info</InputGroup.Text>
                            </InputGroup.Prepend>
                            <FormControl id="partInfo" onChange={this.handlePartInput} placeholder="Extra Info" />
                          </InputGroup>
                        </Form.Group>
                      </Col>
                      <Col lg>
                        <Form.Group className="" controlId="formPartCount">
                          <InputGroup className="mb-2">
                            <InputGroup.Prepend>
                              <InputGroup.Text>Count</InputGroup.Text>
                            </InputGroup.Prepend>
                            <FormControl id="partCount" onChange={this.handlePartInput} placeholder="Count" />
                          </InputGroup>
                        </Form.Group>
                      </Col>
                      <Col lg>
                        <Form.Group className="" controlId="formPartLocation">
                          <InputGroup className="mb-2">
                            <InputGroup.Prepend>
                              <InputGroup.Text>Location</InputGroup.Text>
                            </InputGroup.Prepend>
                            <FormControl id="partLocation" onChange={this.handlePartInput} placeholder="Location" />
                          </InputGroup>
                        </Form.Group>
                      </Col>
                    </Form.Row>
                    <Button className="mt-3" onClick={this.submitPartInventory} variant="success">Submit Part</Button>
                      {(
                        this.state.errorPartInput && 
                        <p class="text-danger">{this.state.errorPartInput}</p>
                      )}
                  </Form>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          <Row className="mt-5">
            <Col sm={12} align="center">
              <Card>
                <Card.Header><h3>Upload Excel or CSV : </h3></Card.Header>
                <Card.Body>
                <Form>
                  <Form.Row className="align-items-center" className="g-2">
                    <Col md>
                      <Form.Group controlId="formFile" className="mb-3">
                        <Form.File
                          id="custom-file"
                          label={this.state.selectedFile ? this.state.selectedFile.name : "CSV or Excel File"}
                          onChange={this.onFileChange}
                          custom
                        />
                      </Form.Group>
                    </Col>
                  </Form.Row>
                  <Button className="mt-3" onClick={this.onFileUpload} variant="success">Submit File</Button>
                </Form>
                </Card.Body>
              </Card>
            </Col>
          </Row>
          <Row className="mt-5">
            <Col sm={12} align="center">
              <Card>
                <Card.Header><h2>Existing Part and Inventories : </h2></Card.Header>
                <Card.Body>
                  <h3>{this.state.partAdded}</h3>
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
