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

const wrapperStyle = { marginRight: "5%", marginLeft: "5%", marginTop: "5%", marginBottom: "5%", textAlign: "center" };

class ParisPage extends Component { 
    
    constructor(props){
        super(props);
        this.state = {
          "sliderValue" : 481,
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
          "evts":[],
          "kings":[],
          "persos":[]
        };
        this.handleGetKing = this.handleGetKing.bind(this);
        this.handleGetMonument = this.handleGetMonument.bind(this);
        this.handleGetEvt = this.handleGetEvt.bind(this);
        this.handleGetPerso = this.handleGetPerso.bind(this);
        this.handleGetKing(481)
        //this.handleGetMonument(300)
        //this.handleGetEvt(300)
        //this.handleGetPerso(300)
    }
    
    handleGetKing(year){
      console.log("http://backend.oursbrindille.fun/personnage/year/"+year)
      let self = this;
      gethttp().get("http://backend.oursbrindille.fun/personnage/year/"+year).end(function(err, res){
          if(err) alert("Erreur lors de la récupération des données sur le serveur : " + err.message);
          else {
            var obj = JSON.parse(res.text);
            console.log(obj)
            if(obj.length > 0){
              console.log("not empty");
              self.setState({kings: obj});
            }
          }
        });
  }

  handleGetMonument(year){
    console.log("http://backend.oursbrindille.fun/test/monument/year/"+year)
    let self = this;
    gethttp().get("http://backend.oursbrindille.fun/test/monument/year/"+year).end(function(err, res){
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
  console.log("http://backend.oursbrindille.fun/test/evenement/year/"+year)
  let self = this;
  gethttp().get("http://backend.oursbrindille.fun/test/evenement/year/"+year).end(function(err, res){
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

handleGetPerso(year){
  console.log("http://backend.oursbrindille.fun/test/personnage/year/"+year)
  let self = this;
  gethttp().get("http://backend.oursbrindille.fun/test/personnage/year/"+year).end(function(err, res){
      if(err) alert("Erreur lors de la récupération des données sur le serveur : " + err.message);
      else {
        var obj = JSON.parse(res.text);
        console.log(obj)
        if(obj.length > 0){
          console.log("not empty");
          self.setState({persos: obj});
        }else{
          self.setState({persos: []});
        }
      }
    });
}
    
    handleChange = sliderValue => {
        this.setState({ sliderValue });
        this.handleGetKing(sliderValue);
        //this.handleGetMonument(sliderValue);
        //this.handleGetEvt(sliderValue);
        //this.handleGetPerso(sliderValue);
      };
    render() 
    { 
        return <div style={{color: 'white'}}>
            <div style={{textAlign:"center"}}><h1>Année : {this.state.sliderValue}</h1></div>
            <div style={wrapperStyle}>
            <p>Choisissez votre date : </p>
            <Slider min={481} max={1792} defaultValue={481} handle={handle} onChange={this.handleChange}/>
            </div>
            <div style={{float: "left", width:"100%", height:"100%"}}>
              <div style={{textAlign: "center", float:"left", width:"100%"}}>
                <div>{this.state.kings.map(king => (<div style={{float: "left", width:"100%", marginBottom: "50px"}}>
                                                      <div style={{minWidth:"300px"}}>
                                                        <div><h1>{king.nom} ({parseInt(king.birthyear)} - {parseInt(king.deathyear)})</h1></div>
                                                        <div>Roi de {parseInt(king.startyear,10)} à {parseInt(king.endyear)}</div>
                                                        <div>Epouse(s) : {king.spouses}</div>
                                                        <div>Père : {king.fatherlabel} - Mère : {king.motherlabel}</div>
                                                        <div>Mort à {king.placeofdeathlabel} {king.mannersofdeath}</div>
                                                        <div>Repose à : {king.placeofburiallabel}</div>
                                                        <br /><br />
                                                      </div>
                                                      <div style={{minWidth: "300px"}}>
                                                        <img src={"http://files.oursbrindille.fun/kings/"+king.urlimage} style={{height: '300px'}}/>
                                                      </div>
                                                    </div>))}</div>
              </div>
            </div>   
        </div>
      } 
}   
  
// Exporting the component 
export default ParisPage; 
