
import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Badge from 'react-bootstrap/Badge';
import Table from 'react-bootstrap/Table';

// Main React Component

class InventoryManagement extends React.Component {
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
      newPartInfo: null,
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
    this.clearOutInventories = this.clearOutInventories.bind(this);
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
    this.handleNewPartInfo = this.handleNewPartInfo.bind(this);
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
        'Content-Type': 'application/json',
        'x-access-token': sessionStorage.getItem('token')
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
      'Content-Type': 'application/json',
      'x-access-token': sessionStorage.getItem('token')
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
        'Content-Type': 'application/json',
        'x-access-token': sessionStorage.getItem('token')
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
      'Content-Type': 'application/json',
      'x-access-token': sessionStorage.getItem('token')
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
        'Content-Type': 'application/json',
        'x-access-token': sessionStorage.getItem('token')
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
      'Content-Type': 'application/json',
      'x-access-token': sessionStorage.getItem('token')
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
        'Content-Type': 'application/json',
        'x-access-token': sessionStorage.getItem('token')
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(Object.keys(data[0]).map((item) => {
        return {part_number : data[0][item].part_number, part_info : data[0][item].part_info}
      }));
      this.setState({
        // parts: this.state.chromebook_parts['brands'][this.state.current_brand][this.state.current_model_name][this.state.current_repair]["parts"]
        // parts: Object.keys(data[0])
        parts: Object.keys(data[0]).map((item) => {
          return {part_number : data[0][item].part_number, part_info : data[0][item].part_info}
        })
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
      body: JSON.stringify({"part_number" : this.state.newPartNumber, "part_info" : this.state.newPartInfo}),
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'x-access-token': sessionStorage.getItem('token')
      }
    })
    .then(response => response.json())
    .then((data) => {
      console.log(Object.keys(data));
      this.setState({
        // parts: this.state.chromebook_parts['brands'][this.state.current_brand][this.state.current_model_name][this.state.current_repair]["parts"]
        // parts: Object.keys(data)
        parts: Object.keys(data[0]).map((item) => {
          return {part_number : data[0][item].part_number, part_info : data[0][item].part_info}
        })
      }, () => {
        this.setState({
          current_parts: this.state.parts,
          newPartNumber: "",
          newPartInfo: ""
        });
      });
    })
    .catch(err => console.log(err));
  }

  fetchInventories(part) {
    // Need to url encode the part var first
    part = encodeURIComponent(part);
    fetch(`${process.env.REACT_APP_API_URL}/get_inventory/${part}`, {
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'x-access-token': sessionStorage.getItem('token')
      }
    })
    .then(response => response.json())
    .then((data) => {
      if(Object.keys(data).length){
          let inventory_state = this.state.inventories.slice();
          console.log(this.state.inventories)
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
      'Content-Type': 'application/json',
      'x-access-token': sessionStorage.getItem('token')
      }
    })
    .then(response => response.json())
    .then((data) => {
      if(Object.keys(data).length){
          // Set this up where I filter out old inventory for current selected part, then
          // push new inventory object in array of inventory,
          // then update inventory presented on page
          let inventory_state = this.state.inventories.filter(item => !(item[part]))
          inventory_state.push(data);
          console.log(inventory_state)
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

  clearOutInventories() {
    this.setState({
        inventories: []
    }, () => {
      this.setState({
          current_inventories: []
      });
    });
  }


  updateInventory(part) {
    console.log(`Added Inventory: ${this.state.newInventory}`)
    // this.clearOutInventories();

    part = encodeURI(part);

    fetch(`${process.env.REACT_APP_API_URL}/get_inventory/${part}`, {
      mode: 'cors',
      method: "PUT",
      body: JSON.stringify({"count" : this.state.current_count, "location_desc" : this.state.current_location}),
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'x-access-token': sessionStorage.getItem('token')
      }
    })
    .then(response => response.json())
    .then((data) => {
      if(Object.keys(data).length){
          // Set this up where I filter out old inventory for current selected part, then
          // push new inventory object in array of inventory,
          // then update inventory presented on page
          let inventory_state = this.state.inventories.filter(item => !(item[part]))
          inventory_state.push(data);
          console.log(inventory_state)
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


// This was working perfect awhile ago, so have no clue.
  useOnePart(part, location) {
    console.log(`changed inventory by one: ${this.state.newInventory}`)

    fetch(`${process.env.REACT_APP_API_URL}/use_part/${part}`, {
      mode: 'cors',
      method: "PATCH",
      body: JSON.stringify({"part_number" : part}),
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'x-access-token': sessionStorage.getItem('token')
      }
    })
    .then(response => response.json())
    .then((data) => {
      if(Object.keys(data).length){
          // Set this up where I filter out old inventory for current selected part, then
          // push new inventory object in array of inventory,
          // then update inventory presented on page
          let inventory_state = this.state.inventories.filter(item => !(item[part]))
          inventory_state.push(data);
          console.log(inventory_state)
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
          'Content-Type': 'application/json',
          'x-access-token': sessionStorage.getItem('token')
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
      newBrandName: event.target.value.trim()
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
      newModelName: event.target.value.trim()
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
      newRepairType: this.state.current_model_name + '-' + event.target.value.trim()
    });
  }

  submitPostRepair(event){
    this.postRepair(this.state.current_model_name);
    // this.setState({
    //   parts: this.state.parts.push(event.target.value),
    //   current_parts: this.state.parts
    // })
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
          this.fetchInventories(part.part_number);
        });
        this.handleInventories(event);
      });




  }

  handleNewPartNumber(event){
    this.setState({
      newPartNumber: event.target.value.trim()
    });
  }

  handleNewPartInfo(event){
    this.setState({
      newPartInfo: event.target.value.trim()
    });
  }

  handleShowAddParts(event){
    this.setState({
      showAddParts: !this.state.showAddParts
    });
  }


  submitPostPart(event) {
    this.postPart(this.state.current_repair);
    // Clear input fields
    document.getElementById('input-part-number').value = "";
    document.getElementById('part-info').value = "";
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
      <div className="InventoryManagement">
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
                              <Form.Control as="input" id="input-add-brand" onChange={this.handlePostBrand}>

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
                                    <Form.Control as="input" id="input-model" placeholder="format:<Model Name>-<Screen Size>-<Model Number> EX: Macbook-Air-13-A1466" onChange={this.handlePostModel}>

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
                                    <Form.Control as="input" id="select-repair-type" placeholder="Do not include model, year, or model number; just part name" onChange={this.handleNewRepairType}>

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
                              <Form.Label> Enter Part Info (This is used to differentiate between parts for differnet versions of a model. For example, Intel, MTK, or AMD versions of the same model.) :  </Form.Label>
                              <Form.Control as="input" id="part-info" onChange={this.handleNewPartInfo}>

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



                            <ListGroup.Item as="li" active>Available Parts for this repair</ListGroup.Item>
                            {/* Table Style*/}
                              <Table striped bordered>
                                <thead>
                                  <tr>
                                    <th>Part Number</th>
                                    <th>Extra Notes</th>
                                    <th>Use One</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {this.state.current_parts.map((item) => {
                                    return <tr>

                                        <th>
                                          {item.part_number}
                                        </th>
                                        <th>
                                          {item.part_info &&
                                            <Badge bg="info">
                                              <p>{ item.part_info }</p>
                                            </Badge>
                                          }
                                        </th>
                                        <th>
                                          <Button className="ml-3" onClick={() => {this.useOnePart(item.part_number)}}>Use One</Button>
                                        </th>
                                    </tr>
                                  })}
                                </tbody>
                              </Table>

                            {/*
                            **** UL list style ***
                            {this.state.current_parts.map((item) => {
                              return <ListGroup.Item as="li">

                                  {item.part_number}
                                  {'   '}
                                  <Button className="ml-3" onClick={() => {this.useOnePart(item.part_number)}}>Use One</Button>
                                  {'   '}
                                  {item.part_info &&
                                    <Badge bg="info">
                                      <p>Notes:</p>
                                      <p>{ item.part_info }</p>
                                    </Badge>
                                  }





                              </ListGroup.Item>

                            })}
                            */}
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
                                          return <option value={part["part_number"]}>{part["part_number"]}</option>
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
                                          return <option value={part["part_number"]}>{part["part_number"]}</option>
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
                            {(this.state.current_inventories.length > 0) ?
                              <>
                                <ListGroup.Item as="li" active>Inventory for parts</ListGroup.Item>

                                  {/*

                                    I just cannot read this. How can I follow something so messy and encapsulated like this?
                                    Both backend and frontend for inventory need to be redesigned. I litterally cannot do anything
                                    with this code.

                                    Well, now it works. Have no clue. I'm not touching this mess right now!!!
                                    */}
                                  <Table striped bordered>
                                  <thead>
                                    <tr>
                                      <td>Part Number</td>
                                      <td>Count</td>
                                      <td>Location</td>
                                    </tr>
                                  </thead>
                                  {this.state.current_inventories.map((inventory) => {
                                    // console.log(Object.keys(inventory).map((part_name) => {
                                    //     return Object.keys(inventory[part_name]).map((location) => {
                                    //         return Object.keys(inventory[part_name][location]).map((count) => {
                                    //             return inventory[part_name][location][count];
                                    //         });
                                    //     });
                                    // }))

        // Object.keys(map).map((key) => map[key]);
                                    let array = Object.keys(inventory).map((part_name) => {
                                        return Object.keys(inventory[part_name]).map((location) => {
                                          let count_name = inventory[part_name][location]["count"];
                                          let location_name = inventory[part_name][location]["location_desc"];
                                          let location_id = location;
                                          let part_item_name = part_name;

                                          return <tr><td>{part_item_name}</td><td>{count_name}</td><td>{location_name}</td></tr>
                                            // return Object.keys(inventory[part_name][location]).map((count, location_desc) => {
                                            //     let count_name = inventory[part_name][location][count];
                                            //     let location_name = inventory[part_name][location][location_desc];
                                            //     let location_id = location;
                                            //     let part_item_name = part_name;
                                            //     return <ListGroup.Item as="li">Part Number: {part_item_name} | Location_id: {location_id} | Count: {count_name} | Location_name: {location_name}</ListGroup.Item>
                                            // });
                                        });
                                    })

                                    return <tbody>{array}</tbody>
                                  })}
                                </Table>
                              </>
                              :
                                <> </>
                            }
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

export default InventoryManagement;
