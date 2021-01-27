import './App.css';
import React from 'react';
import ReactDOM from 'react-dom';

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
      console.log(data[0].brands["Dell"].filter((model) => {
        return model.model_name === "REPAIR-DELL-CB1C13"
      })[0].repairs.map((repair) => {
        return repair.repair_type
      }));
      this.setState({
        chromebook_parts: data
      }, () => {
        const brands = Object.keys(this.state.chromebook_parts[0].brands);
        this.setState({
          brands: brands
        })
      });
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
        current_path: this.state.chromebook_parts[0].brands[this.state.current_brand]
      }, () => {
        this.setState({
          models: this.state.current_path.map((model) => {
            return model.model_name;
          })
        });
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
        current_path: this.state.chromebook_parts[0].brands[this.state.current_brand].filter((model) => {
                      return model.model_name === this.state.current_model_name
                    })[0]
      }, () => {
        this.setState({
          repairs: this.state.current_path.repairs.map((repair) => {
            return repair.repair_type
          })
        });
      });
    });
  }
  handleModelNumber(event){

  }
  handleRepair(event){
    this.setState({
      current_repair: event.target.value,
    }, () => {
      this.setState({
        current_path: this.state.chromebook_parts[0].brands[this.state.current_brand].filter((model) => {
                      return model.model_name === this.state.current_model_name
                    })[0].repairs.filter((repair) => {
                      return repair.repair_type === this.state.current_repair
                    })
      }, () => {
        this.setState({
          parts: this.state.current_path[0].parts
        });
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
        <form>
          <label>Choose a Brand:</label>
          <select id="select-brand" onChange={this.handleBrand}>
            <option disabled="disabled" selected="selected">Select a Brand</option>
            {
              this.state.brands.map((brand) => {
                return <option value={brand}>{brand}</option>
              })
            }
          </select>
            {this.state.current_brand  ?
                <div>
                  <label> Choose Model </label>
                  <select id="select-model" onChange={this.handleModelName}>
                    <option disabled="disabled" selected="selected">Select a Model</option>
                    {
                      this.state.models.map((model) => {
                        return <option value={model}>{model}</option>
                      })
                    }
                  </select>
                </div>
              :
                <br />

            }
            <br />
            {
              this.state.current_model_name ?
                <div>
                  <label>Choose Repair Type</label>
                  <select id="select-repair" onChange={this.handleRepair}>
                    <option value="" selected disabled hidden>Choose here</option>
                    {
                          this.state.repairs.map((repair) => {
                            return <option value={repair}>{repair}</option>
                          })
                    }
                  </select>
                </div>
              :
                <br />
            }
            <button onClick={this.handleParts}>Find parts for this repair</button>
        </form>
        {
          this.state.current_parts ?
            <div>
              <h3>Avaibale Parts for this repair</h3>
              <ul>
                {this.state.current_parts.map((part) => {
                  return <li>{part}</li>
                })}
              </ul>
            </div>
          :
            <br />
        }
      </div>
    );
  }
}

export default App;
