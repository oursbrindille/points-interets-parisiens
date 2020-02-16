import React, {Component} from 'react'; 

import 'rc-slider/assets/index.css';
import 'rc-tooltip/assets/bootstrap.css';
import Tooltip from 'rc-tooltip';
import Slider from 'rc-slider';

export function gethttp(){
    var http = require('superagent');
    return http;
}

const createSliderWithTooltip = Slider.createSliderWithTooltip;
const Range = createSliderWithTooltip(Slider.Range);
const Handle = Slider.Handle;


const handle = (props) => {
  const { value, dragging, index, ...restProps } = props;
  return (
    <Tooltip
      prefixCls="rc-slider-tooltip"
      overlay={value}
      visible={dragging}
      placement="top"
      key={index}
    >
      <Handle value={value} {...restProps} />
    </Tooltip>
  );
};

const wrapperStyle = { marginRight: 150, marginLeft: 150, marginTop: 50, marginBottom: 50 };

class KingPage extends Component { 
    
    constructor(props){
        super(props);
        this.state = {
          "sliderValue" : 987,
          "res" : "a",
          "king": "",
          "startYear": 0,
          "endYear": 0,
          "birthYear": 0,
          "deathYear": 0,
          "spouses": "",
          "placeOfDeathLabel": "",
          "placeOfBurialLabel": "",
          "fatherLabel": "",
          "motherLabel":"",
          "mannersOfDeath":"",
          "monuments":[],
          "evts":[]
        };
        this.handleGetKing = this.handleGetKing.bind(this);
        this.handleGetMonument = this.handleGetMonument.bind(this);
        this.handleGetEvt = this.handleGetEvt.bind(this);
        this.handleGetKing(987)
        this.handleGetMonument(987)
        this.handleGetEvt(987)
    }
    
    handleGetKing(year){
      console.log("http://localhost:5000/king/year/"+year)
      let self = this;
      gethttp().get("http://localhost:5000/king/year/"+year).end(function(err, res){
          if(err) alert("Erreur lors de la récupération des données sur le serveur : " + err.message);
          else {
            var obj = JSON.parse(res.text);
            console.log(obj)
            self.setState({king: obj[0].nom});
            self.setState({startYear: obj[0].startYear});
            self.setState({endYear: obj[0].endYear});
            self.setState({birthYear: obj[0].birthYear});
            self.setState({deathYear: obj[0].deathYear});
            self.setState({spouses: obj[0].spouses});
            self.setState({placeOfDeathLabel: obj[0].placeOfDeathLabel});
            self.setState({placeOfBurialLabel: obj[0].placeOfBurialLabel});
            self.setState({fatherLabel: obj[0].fatherLabel});
            self.setState({motherLabel: obj[0].motherLabel});
            if(obj[0].mannersOfDeath != null){
              self.setState({mannersOfDeath: "de "+obj[0].mannersOfDeath});
            }
          }
        });
  }

  handleGetMonument(year){
    console.log("http://localhost:5000/monument/year/"+year)
    let self = this;
    gethttp().get("http://localhost:5000/monument/year/"+year).end(function(err, res){
        if(err) alert("Erreur lors de la récupération des données sur le serveur : " + err.message);
        else {
          var obj = JSON.parse(res.text);
          console.log(obj)
          if(obj.length > 0){
            console.log("not empty");
            self.setState({monuments: obj});
          }
        }
      });
}


handleGetEvt(year){
  console.log("http://localhost:5000/evenement/year/"+year)
  let self = this;
  gethttp().get("http://localhost:5000/evenement/year/"+year).end(function(err, res){
      if(err) alert("Erreur lors de la récupération des données sur le serveur : " + err.message);
      else {
        var obj = JSON.parse(res.text);
        console.log(obj)
        if(obj.length > 0){
          console.log("not empty");
          self.setState({evts: obj});
        }else{
          self.setState({evts: []});
        }
      }
    });
}
    
    handleChange = sliderValue => {
        this.setState({ sliderValue });
        this.handleGetKing(sliderValue);
        this.handleGetMonument(sliderValue);
        this.handleGetEvt(sliderValue);
      };
    render() 
    { 
        return <div style={{color: 'white'}}>
            <div style={wrapperStyle}>
            <p>Choisissez votre date : </p>
            <Slider min={987} max={1773} defaultValue={987} handle={handle} onChange={this.handleChange}/>
            <div style={{textAlign:"center"}}><h1>Année : {this.state.sliderValue}</h1></div>
            </div>
            <div style={{float: "left", width:"100%", height:"100%"}}>
              <div style={{textAlign: "center", float:"left", width:"50%"}}>
                <div><h1>Chef d'état</h1></div>
                <div><h1>{this.state.king}({this.state.birthYear} - {this.state.deathYear})</h1></div>
                <div>Roi de {this.state.startYear} à {this.state.endYear}</div>
                <div>Epouse(s) : {this.state.spouses}</div>
                <div>Père : {this.state.fatherLabel} - Mère : {this.state.motherLabel}</div>
                <div>Mort à {this.state.placeOfDeathLabel} {this.state.mannersOfDeath}</div>
                <div>Repose à : {this.state.placeOfBurialLabel}</div>
                <br /><br />
              </div>
              <div style={{textAlign: "center", float:"left", width:"50%"}}>
                <div><h1>Evenement en cours</h1></div>
                <div>{this.state.evts.map(evt => (<div>- {evt.evenement}</div>))}</div>
              </div>
            </div>         
            <div style={{textAlign: "center", float:"left", width:"100%"}}>
                <div><h1>Monuments Parisiens</h1></div>
                <div>{this.state.monuments.map(monument => (<div>{monument.nom}</div>))}</div>
            </div>
        </div>;
      } 
}   
  
// Exporting the component 
export default KingPage; 
