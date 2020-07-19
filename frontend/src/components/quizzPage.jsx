import React, {Component} from 'react'; 

import 'rc-slider/assets/index.css';
import 'rc-tooltip/assets/bootstrap.css';
import Tooltip from 'rc-tooltip';
import Slider from 'rc-slider';
import Popup from "reactjs-popup";
import { Button, Modal } from 'react-bootstrap'

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

class QuizzPage extends Component { 
    
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
          "king":[],
          "quizzKings":[],
          "quizzYear":0,
          "persos":[],
          "popupopen":false,
          "answerImage": "",
          "answerTitle":"",
          "answerCorpus":"",
          "answerKing":"",
          "showHide" : false
        };
        this.handleGetKings = this.handleGetKings.bind(this);
        this.handleGetKing = this.handleGetKing.bind(this);
        this.correction = this.correction.bind(this);
        this.handleGetKings();
        this.newQuizz = this.newQuizz.bind(this);
    }
    
    handleGetKings(){
        console.log("http://backend.oursbrindille.fun/personnage")
        let self = this;
        gethttp().get("http://backend.oursbrindille.fun/personnage").end(function(err, res){
            if(err) alert("Erreur lors de la récupération des données sur le serveur : " + err.message);
            else {
              var obj = JSON.parse(res.text);
              console.log(obj)
              if(obj.length > 0){
                console.log("not empty");

                //only since hugues capet
                function filter_kings(kings) {
                  return kings.startyear >= 987;
                }

                var filtered = obj.filter(filter_kings);

                self.setState({kings: filtered});

                self.newQuizz();
              }
            }
          }); 
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
              self.setState({king: obj});

              
              console.log(self.state.king);
              var arr = [];
              while(arr.length < 3){
                  var r = Math.floor(Math.random() * self.state.kings.length);
                  if(self.state.kings[r].id_personnage !== self.state.king[0].id_personnage){
                    if(arr.indexOf(r) === -1) arr.push(r);
                  }
              }
              for (var i = 0; i < self.state.kings.length; i++) {
                if(self.state.kings[i].id_personnage == self.state.king[0].id_personnage){
                  arr.push(i);
                }
              }
              console.log(arr);
              
              var quizzKings = [];
              for (var i = 0; i < self.state.kings.length; i++) {
                if(arr.includes(i)){
                  quizzKings.push(self.state.kings[i]);
                }
              }

              function shuffle(a) {
                var j, x, i;
                for (i = a.length - 1; i > 0; i--) {
                    j = Math.floor(Math.random() * (i + 1));
                    x = a[i];
                    a[i] = a[j];
                    a[j] = x;
                }
                return a;
            }

              quizzKings = shuffle(quizzKings);
              console.log(quizzKings);
              
              self.setState({quizzKings: quizzKings});

            }
          }
        });
  }

    newQuizz(){
        this.setState({showHide: false});
        console.log(this.state.kings);
        
        var year = Math.floor(Math.random() * (1792-987))+987;
        this.setState({quizzYear: year});
        this.handleGetKing(year)
    }

    correction(id){
      this.setState({showHide: true});
      if(id == this.state.king[0].id_personnage){
        console.log("yesss")
        this.setState({answerImage: "crown.png"});
        this.setState({answerTitle: "Bravo !"});
        this.setState({answerCorpus: "c'est une excellente réponse !"});
        this.setState({answerKing: "C'était bien le roi "+this.state.king[0].nom});
      }else{
        console.log("noooo")
        this.setState({answerImage: "guillotine.png"});
        this.setState({answerTitle: "Raté !"});
        this.setState({answerCorpus: "Tu feras mieux la prochaine fois..."});
        this.setState({answerKing: "La bonne réponse était "+this.state.king[0].nom});
      }
    }
    
    handleModalShowHide() {
      this.setState({ showHide: !this.state.showHide })
  }

    render() 
    { 
        return <div style={{color: 'white'}}>
          <br/>            
          <div style={{textAlign:"center"}}><h1>Année : {this.state.quizzYear}</h1></div>
            <div style={{float: "left", width: "100%", margin:"auto"}}>
              <div style={{textAlign: "center", float:"left", width:"100%"}}>
                <div>
                  {this.state.quizzKings.map(king => (
                    <div style={{padding: "auto", float: "left", minWidth:"300px", margin: "50px"}}>
                      <div style={{minWidth: "300px"}}>
                        <img src={"http://files.oursbrindille.fun/kings/"+king.urlimage} style={{height: '300px'}}/>
                      </div>
                      <br/>
                      <button class="btn btn-dark" onClick={() => this.correction(king.id_personnage)}>{king.nom}</button>
                    </div>))}</div>
              </div>
              <br /><br/><br/>
            </div>  

            <Modal show={this.state.showHide}>
                <Modal.Header closeButton onClick={() => this.handleModalShowHide()}>
                <Modal.Title>{this.state.answerTitle}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                  <div style={{textAlign: "center"}}>
                    <img src={"http://files.oursbrindille.fun/utils/"+this.state.answerImage} style={{width: '300px'}}/>
                    <br /><br/><br/>
                    {this.state.answerCorpus}
                    <br/><br/><br/>
                  </div>
                </Modal.Body>
                <Modal.Footer>
                <Button variant="secondary" onClick={() => this.handleModalShowHide()}>
                    Réessayer
                </Button>
                <Button variant="success" onClick={() => this.newQuizz()}>
                    Nouveau Quizz
                </Button>
                </Modal.Footer>
            </Modal>

        </div>
      } 
}   
  
// Exporting the component 
export default QuizzPage; 
