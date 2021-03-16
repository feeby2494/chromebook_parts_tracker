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
import ButtonGroup from 'react-bootstrap/ButtonGroup'

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
      inventories: [],
      locations: [],
      current_brand : null,
      current_path: '',
      current_model_name : null,
      current_model_number : null,
      current_repair : null,
      current_parts : [],
      current_inventories: [],
      current_part_selected: null,
      current_location: null,
      current_count: null,
      newBrandName: null,
      newModelName: null,
      newRepairType: null,
      newRepairArea: null,
      newPartNumber: null,
      newInventory: null,
      showAddParts: false,
      showAddInventory: false,
      showUpdateInventory: false,
    }
    this.getChromebookJSON = this.getChromebookJSON.bind(this);
    this.fetchBrands = this.fetchBrands.bind(this);
    this.postBrand = this.postBrand.bind(this);
    this.fetchModels = this.fetchModels.bind(this);
    this.postModel = this.postModel.bind(this);
    this.fetchRepairs = this.fetchRepairs.bind(this);
    this.postRepair = this.postRepair.bind(this);
    this.fetchParts = this.fetchParts.bind(this);
    this.postPart = this.postPart.bind(this);
    this.fetchInventories = this.fetchInventories.bind(this);
    this.postInventory = this.postInventory.bind(this);
    this.updateInventory = this.updateInventory.bind(this);
    this.fetchLocations = this.fetchLocations.bind(this);
    this.handleBrand = this.handleBrand.bind(this);
    this.handlePostBrand = this.handlePostBrand.bind(this);
    this.submitPostBrand = this.submitPostBrand.bind(this);
    this.handleModelName = this.handleModelName.bind(this);
    this.handlePostModel = this.handlePostModel.bind(this);
    this.submitPostModel = this.submitPostModel.bind(this);
    this.handleRepair = this.handleRepair.bind(this);
    this.handleNewRepairArea = this.handleNewRepairArea.bind(this);
    this.handleNewRepairType = this.handleNewRepairType.bind(this);
    this.submitPostRepair = this.submitPostRepair.bind(this);
    this.handleParts = this.handleParts.bind(this);
    this.handleNewPartNumber = this.handleNewPartNumber.bind(this);
    this.handleShowAddParts = this.handleShowAddParts.bind(this);
    this.submitPostPart = this.submitPostPart.bind(this);
    this.handleShowAddInventory = this.handleShowAddInventory.bind(this);
    this.handleCurrentPartSelected = this.handleCurrentPartSelected.bind(this);
    this.handleInventories = this.handleInventories.bind(this);
    this.handleLocation = this.handleLocation.bind(this);
    this.handlePostInventory = this.handlePostInventory.bind(this);
    this.submitPostInventory = this.submitPostInventory.bind(this);
    this.handleShowUpdateInventory = this.handleShowUpdateInventory.bind(this);
    this.handleUpdateInventory = this.handleUpdateInventory.bind(this);
    this.submitUpdateInventory = this.submitUpdateInventory.bind(this);
  }

  //                         METHODS
  getChromebookJSON(event) {
    fetch(`${process.env.REACT_APP_API_URL}/chromebook_parts`, {
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
    // this.getChromebookJSON();
    this.fetchBrands();
  }

  fetchBrands() {
    fetch(`${process.env.REACT_APP_API_URL}/get_brands`, {
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(data.brands);
      this.setState({
        brands: data.brands
      })
    });
  }

  postBrand() {
    console.log(`Added brand: ${this.state.newBrandName}`)

    fetch(`${process.env.REACT_APP_API_URL}/get_brands`, {
      mode: 'cors',
      method: "POST",
      body: JSON.stringify({"brand_name" : this.state.newBrandName}),
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(data.brands);
      this.setState({
        brands: data.brands
      })
    })
    .catch(err => console.log(err));
  }

  fetchModels(brand) {
    fetch(`${process.env.REACT_APP_API_URL}/get_models/${brand}`, {
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(data.models)
      this.setState({
        // models: Object.keys(this.state.chromebook_parts['brands'][this.state.current_brand])
        models: data.models
      });
    });
  }

  postModel(brand) {
    console.log(`Added brand: ${this.state.newModelName}`)

    fetch(`${process.env.REACT_APP_API_URL}/get_models/${brand}`, {
      mode: 'cors',
      method: "POST",
      body: JSON.stringify({"model_name" : this.state.newModelName}),
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(data.models)
      this.setState({
        // models: Object.keys(this.state.chromebook_parts['brands'][this.state.current_brand])
        models: data.models
      });
    })
    .catch(err => console.log(err));
  }

  fetchRepairs(model) {
    fetch(`${process.env.REACT_APP_API_URL}/get_repairs/${model}`, {
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(Object.keys(data));
      this.setState({
        // repairs: Object.keys(this.state.chromebook_parts['brands'][this.state.current_brand][this.state.current_model_name])
        repairs: Object.keys(data)
      });
    });
  }

  postRepair(model) {
    console.log(`Added Repair: ${this.state.newRepairType}`)

    fetch(`${process.env.REACT_APP_API_URL}/get_repairs/${model}`, {
      mode: 'cors',
      method: "POST",
      body: JSON.stringify({"repair_type" : this.state.newRepairType, "repair_area": this.state.newRepairArea}),
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(Object.keys(data));
      this.setState({
        // repairs: Object.keys(this.state.chromebook_parts['brands'][this.state.current_brand][this.state.current_model_name])
        repairs: Object.keys(data)
      })
    })
    .catch(err => console.log(err));
  }

  fetchParts(repair) {
    fetch(`${process.env.REACT_APP_API_URL}/get_parts/${repair}`, {
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(Object.keys(data));
      this.setState({
        // parts: this.state.chromebook_parts['brands'][this.state.current_brand][this.state.current_model_name][this.state.current_repair]["parts"]
        parts: Object.keys(data[0])
      }, () => {
        this.setState({
          current_parts: this.state.parts
        });
      });
    });
  }

  postPart(repair) {
    console.log(`Added Part: ${this.state.newPartNumber}`)

    fetch(`${process.env.REACT_APP_API_URL}/get_parts/${repair}`, {
      mode: 'cors',
      method: "POST",
      body: JSON.stringify({"part_number" : this.state.newPartNumber}),
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(Object.keys(data));
      this.setState({
        // parts: this.state.chromebook_parts['brands'][this.state.current_brand][this.state.current_model_name][this.state.current_repair]["parts"]
        parts: Object.keys(data[0])
      }, () => {
        this.setState({
          current_parts: this.state.parts
        });
      });
    })
    .catch(err => console.log(err));
  }

  fetchInventories(part) {
    fetch(`${process.env.REACT_APP_API_URL}/get_inventory/${part}`, {
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      if(Object.keys(data).length){
          let inventory_state = this.state.inventories.slice();
          inventory_state.push(data)
          console.log("inventory: " + inventory_state)

          this.setState({
              inventories: inventory_state
          }, () => {
            this.setState({
                current_inventories: this.state.inventories
            });
          });
      }
    });
  }
  // fetchLocations(inventory) {
  //   fetch(`${process.env.REACT_APP_API_URL}/get_locations/${inventory}`, {
  //     mode: 'cors',
  //     headers: {
  //       'Content-Type': 'application/json'
  //     }
  //   })
  //   .then(response => response.json())
  //   .then((data) => {
  //     console.log(Object.keys(data));
  //     return Object.keys(data);
  //   });
  // }

  postInventory(part) {
    console.log(`Added Inventory: ${this.state.newInventory}`)

    fetch(`${process.env.REACT_APP_API_URL}/get_inventory/${part}`, {
      mode: 'cors',
      method: "POST",
      body: JSON.stringify({"count" : this.state.current_count, "location_desc" : this.state.current_location}),
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      if(Object.keys(data).length){
          let inventory_state = this.state.inventories.slice();
          inventory_state.push(data)
          console.log("inventory: " + inventory_state)

          this.setState({
              inventories: inventory_state
          }, () => {
            this.setState({
                current_inventories: this.state.inventories
            });
          });
      }
    });
  }

  updateInventory(part) {
    console.log(`Added Inventory: ${this.state.newInventory}`)

    fetch(`${process.env.REACT_APP_API_URL}/get_inventory/${part}`, {
      mode: 'cors',
      method: "PATCH",
      body: JSON.stringify({"count" : this.state.current_count, "location_desc" : this.state.current_location}),
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then((data) => {
      if(Object.keys(data).length){
          let inventory_state = this.state.inventories.slice();
          inventory_state.push(data)
          console.log("inventory: " + inventory_state)

          this.setState({
              inventories: inventory_state
          }, () => {
            this.setState({
                current_inventories: this.state.inventories
            });
          });
      }
    });
  }

  fetchLocations() {
    fetch(`${process.env.REACT_APP_API_URL}/get_locations/`, {
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then((data) => {
        this.setState({
          locations : Object.keys(data)
        });
      });
  }

  handleBrand(event){
    this.setState({
      current_brand: event.target.value,
      current_repair: null,
      parts: null,
      inventories: [],
      current_parts: null,
      current_model_name: null,
      current_inventories: [],
      showAddParts: false
    }, () => {
      if (this.state.current_brand !== "add_brand") {
        this.fetchModels(this.state.current_brand);
      }

      // this.setState({
      //   // models: Object.keys(this.state.chromebook_parts['brands'][this.state.current_brand])
      //   models: this.fetchModels(this.state.current_brand)
      // });
    });
  }

  handlePostBrand(event){
    console.log(event.target.value);
    this.setState({
      newBrandName: event.target.value
    });
  }

  submitPostBrand(event){
    this.postBrand();
  }

  handleModelName(event){
    this.setState({
      current_model_name: event.target.value,
      current_parts: null,
      current_repair: null,
      current_inventories: [],
      parts: null,
      inventories: [],
      showAddParts: false
    }, () => {
      this.fetchRepairs(this.state.current_model_name)
    });
  }

  handlePostModel(event){
    console.log(event.target.value);
    this.setState({
      newModelName: event.target.value
    });
  }

  submitPostModel(event){
    this.postModel(this.state.current_brand);
  }

  handleRepair(event){
    this.setState({
      current_repair: event.target.value,
      showAddParts: false,
      showUpdateInventory: false,
      showAddInventory: false
    }, () => {
      this.fetchRepairs(this.state.current_model_name);
      this.fetchParts(this.state.current_repair);
      this.fetchLocations();
    });
  }

  handleNewRepairArea(event){
    this.setState({
      newRepairArea: event.target.value
    });
  }

  handleNewRepairType(event){
    this.setState({
      newRepairType: event.target.value
    });
  }

  submitPostRepair(event){
    this.postRepair(this.state.current_model_name);
  }

  handleParts(event){
    event.preventDefault();
    this.setState({
      current_parts: this.state.parts,
      current_inventories: [],
      inventories: []
    }, () => {
        // Need to handle inventories:
        this.state.current_parts.map((part) => {
          this.fetchInventories(part);
        });
        this.handleInventories(event);
      });




  }

  handleNewPartNumber(event){
    this.setState({
      newPartNumber: event.target.value
    });
  }

  handleShowAddParts(event){
    this.setState({
      showAddParts: !this.state.showAddParts
    });
  }


  submitPostPart(event) {
    this.postPart(this.state.current_repair);
  }

handleShowAddInventory(event) {
  console.log(` the part is: ${this.props.children}`)
  this.setState({
    showAddInventory: !this.state.showAddInventory
  });
}

  handleInventories(event){
      this.setState({
          current_inventories: this.state.inventories
      });
  }

  handleCurrentPartSelected(event){
    this.setState({
      current_part_selected: event.target.value
    });
  }

  handleLocation(event){
    this.setState({
      current_location: event.target.value,
    });
  }

  handlePostInventory(event){
    this.setState({
      current_count: event.target.value
    });
  }

  submitPostInventory(event) {
    this.postInventory(this.state.current_part_selected)
  }

  handleShowUpdateInventory(event){
    console.log(` the part is: ${this.props.children}`)
    this.setState({
      showUpdateInventory: !this.state.showUpdateInventory
    });
  }

  handleUpdateInventory(event){
    this.setState({
      current_count: event.target.value
    });
  }

  submitUpdateInventory(event) {
    this.updateInventory(this.state.current_part_selected)
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
                      <option value="add_brand">Add a New Brand</option>
                    </Form.Control>
                      {(this.state.current_brand === "add_brand") ?
                        <div>
                          <Card>
                            <Card.Body>
                              <Form.Label> Add a New Brand </Form.Label>
                              <Form.Control as="input" id="input-model" onChange={this.handlePostBrand}>

                              </Form.Control>
                              <Button onClick={this.submitPostBrand} variant="success">Add</Button>
                            </Card.Body>
                          </Card>
                        </div>
                        :
                        <br />
                      }

                      {(this.state.current_brand && this.state.current_brand !== "add_brand")  ?
                          <div>
                            <Form.Label> Choose Model </Form.Label>
                            <Form.Control as="select" id="select-model" onChange={this.handleModelName}>
                              <option disabled="disabled" selected="selected">Select a Model</option>
                              {
                                this.state.models.map((model) => {
                                  return <option value={model}>{model}</option>
                                })
                              }
                              <option value="add_model">Add Model for this Brand</option>
                            </Form.Control>
                            {(this.state.current_model_name === "add_model") ?
                              <div>
                                <Card>
                                  <Card.Body>
                                    <Form.Label> New Model Name </Form.Label>
                                    <Form.Control as="input" id="input-model" onChange={this.handlePostModel}>

                                    </Form.Control>
                                    <Button onClick={this.submitPostModel} variant="success">Add</Button>
                                  </Card.Body>
                                </Card>
                              </div>
                              :
                              <br />
                            }
                          </div>
                        :
                          <br />

                      }
                      <br />
                      {
                        (this.state.current_model_name && this.state.current_model_name !== "add_model") ?
                          <div>
                            <Form.Label>Choose Repair Type</Form.Label>
                            <Form.Control as="select" id="select-repair" onChange={this.handleRepair}>
                              <option disabled="disabled" selected="selected">Select a Repair</option>
                              {
                                    this.state.repairs.map((repair) => {
                                      return <option value={repair}>{repair}</option>
                                    })
                              }
                              <option value="add_repair">Add New Repair Type</option>
                            </Form.Control>
                            {(this.state.current_repair === "add_repair") ?
                              <div>
                                <Card>
                                  <Card.Body>
                                    <Form.Label> New Repair Area </Form.Label>
                                    <Form.Control as="select" id="select-repair-area" onChange={this.handleNewRepairArea}>
                                      <option disabled="disabled" selected="selected">Choose between Display or Topcase Assembly</option>
                                      <option value="Topcase Assembly">Topcase Assembly</option>
                                      <option value="Display Assembly">Display Assembly</option>
                                    </Form.Control>
                                    <Form.Label> New Repair Type </Form.Label>
                                    <Form.Control as="input" id="select-repair-type" onChange={this.handleNewRepairType}>

                                    </Form.Control>
                                    <Button onClick={this.submitPostRepair} variant="success">Add</Button>
                                  </Card.Body>
                                </Card>
                              </div>
                              :
                              <br />
                            }
                          </div>
                        :
                          <br />
                      }
                      {
                        (this.state.current_repair && this.state.current_repair !== "add_repair") ?
                          <ButtonGroup aria-label="Parts for this Repair">
                            <Button className="mt-2 mr-2" variant="info" onClick={this.handleParts}>Check Inventory for this repair</Button>
                            <Button className="mt-2" variant="success" onClick={this.handleShowAddParts}>Add parts for this repair</Button>
                          </ButtonGroup>
                        :
                          <br />
                      }
                      {
                        (this.state.showAddParts) ?
                          <div>
                          <Card>
                            <Card.Body>
                              <Form.Label> New Part Number </Form.Label>
                              <Form.Control as="input" id="input-part-number" onChange={this.handleNewPartNumber}>

                              </Form.Control>
                              <Button onClick={this.submitPostPart} variant="success">Add</Button>
                            </Card.Body>
                          </Card>
                          </div>
                        :
                          <br />

                      }
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
                      (this.state.current_parts.length > 0) ?
                        <div>
                          <ListGroup as="ul">
                            <ListGroup.Item as="li" active>Avaibale Parts for this repair</ListGroup.Item>
                            {this.state.current_parts.map((part) => {
                              return <ListGroup.Item as="li">

                                  {part}


                              </ListGroup.Item>
                            })}
                            <ButtonGroup aria-label="Inventory for this Part">
                              <Button className="mt-2 mr-2" onClick={this.handleShowUpdateInventory} variant="warning">Update Inventory for this part</Button>
                              <Button className="mt-2" onClick={this.handleShowAddInventory} variant="success">Add Inventory for this part</Button>
                            </ButtonGroup>
                            {
                              (this.state.showAddInventory) ?
                                <div>
                                <Card>
                                  <Card.Body>
                                    <Form.Label> Select Part to add Inventory to </Form.Label>
                                    <Form.Control as="select" id="select-part_name" onChange={this.handleCurrentPartSelected}>
                                      <option value="" selected disabled hidden>Choose here</option>
                                      {
                                            this.state.parts.map((part) => {
                                              return <option value={part}>{part}</option>
                                            })
                                      }
                                    </Form.Control>
                                    <Form.Label> Location of inventory </Form.Label>
                                    <Form.Control as="input" id="input-location" onChange={this.handleLocation}>

                                    </Form.Control>
                                    <Form.Control as="select" id="select-location" onChange={this.handleLocation}>
                                      <option value="" selected disabled hidden>Choose here</option>
                                      {
                                            this.state.locations.map((location) => {
                                              return <option value={location}>{location}</option>
                                            })
                                      }
                                      <option value="add_location">Add New Location</option>
                                    </Form.Control>
                                    <Form.Label> Count of inventory </Form.Label>
                                    <Form.Control as="input" id="input-inventory" onChange={this.handlePostInventory}>

                                    </Form.Control>
                                    <Button onClick={this.submitPostInventory} variant="success">Submit new count</Button>
                                  </Card.Body>
                                </Card>
                                </div>
                              :
                                <p> </p>
                            }
                            {
                              (this.state.showUpdateInventory) ?
                                <div>
                                <Card>
                                  <Card.Body>
                                    <Form.Label> Select Part to add Inventory to </Form.Label>
                                    <Form.Control as="select" id="select-part_name" onChange={this.handleCurrentPartSelected}>
                                      <option value="" selected disabled hidden>Choose here</option>
                                      {
                                            this.state.parts.map((part) => {
                                              return <option value={part}>{part}</option>
                                            })
                                      }
                                    </Form.Control>
                                    <Form.Label> New Location of inventory </Form.Label>
                                    <Form.Control as="input" id="input-location" onChange={this.handleLocation}>

                                    </Form.Control>
                                    <Form.Control as="select" id="select-location" onChange={this.handleLocation}>
                                      <option value="" selected disabled hidden>Choose here</option>
                                      {
                                            this.state.locations.map((location) => {
                                              return <option value={location}>{location}</option>
                                            })
                                      }
                                      <option value="add_location">Add New Location</option>
                                    </Form.Control>
                                    <Form.Label> New Count of inventory </Form.Label>
                                    <Form.Control as="input" id="input-inventory" onChange={this.handleUpdateInventory}>

                                    </Form.Control>
                                    <Button onClick={this.submitUpdateInventory} variant="success">Submit new count</Button>
                                  </Card.Body>
                                </Card>
                                </div>
                              :
                                <p> </p>
                            }
                            <ListGroup.Item as="li" active>Inventory for parts</ListGroup.Item>
                            {this.state.current_inventories.map((inventory) => {
                              console.log(Object.keys(inventory).map((part_name) => {
                                  return Object.keys(inventory[part_name]).map((location) => {
                                      return Object.keys(inventory[part_name][location]).map((count) => {
                                          return inventory[part_name][location][count];
                                      });
                                  });
                              }))

  // Object.keys(map).map((key) => map[key]);
                              let array = Object.keys(inventory).map((part_name) => {
                                  return Object.keys(inventory[part_name]).map((location) => {
                                      return Object.keys(inventory[part_name][location]).map((count) => {
                                          let count_name = inventory[part_name][location][count];
                                          let location_name = location;
                                          let part_item_name = part_name;
                                          return <ListGroup.Item as="li">Part Number: {part_item_name} | location_id: {location_name} | Count: {count_name} </ListGroup.Item>
                                      });
                                  });
                              })

                              return <ListGroup.Item as="li">{array}</ListGroup.Item>
                            })}
                          </ListGroup>
                        </div>
                      :
                        <br />
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
