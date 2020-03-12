import React, {Component} from 'react'; 
import ReactDOM from 'react-dom';
import mapboxgl from 'mapbox-gl';
import { Timeline, TimelineItem }  from 'vertical-timeline-component-for-react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';


mapboxgl.accessToken = 'pk.eyJ1Ijoic2Fib3N0aXgiLCJhIjoiY2p6Y3BkdnJ4MDd2czNjbWdsYXB4MTJoNSJ9.U65hBBejoDAAJH5wrdLejg';

var count = 0
var baseURL = process.env.REACT_APP_BACKEND_SERVER_URL

export function gethttp(){
  var http = require('superagent');
  return http;
}

console.log("toto")

console.log(baseURL)

class MobilePageIndex extends Component { 
    
    constructor(props) {
        super(props);
        this.state = {
        lng: 2.3038,
        lat: 48.8422,
        zoom: 16.5,
        instances:[],
        ownInstance:[],
        rois:[],
        personnages:[],
        evenements:[],
        headerMessage:"",
        secondMessage:"",
        urlImage: "",
        isImage: false,
        baseImageUrl:"../images/kings/",
        showBox1: false,
        showMenu: false,
        showKing: false,
        showCharacter: false,
        showMonument: false,
        showObject: false,
        showEvent: false,
        showThing: false
    };


        fetch(baseURL+'instances/generate')
        .then(res => res.json())
        .then((data) => {
          this.setState({ instances: data })
        })
        .catch(console.log)

        
        fetch(baseURL+'catch/user/1')
        .then(res => res.json())
        .then((data) => {
          this.setState({ ownInstance: data })
        })
        .catch(console.log)

        
        fetch(baseURL+'personnage/start/400/end/600')
        .then(res => res.json())
        .then((data) => {
          var persos = []
          var kings = []
          for (var i = 0; i < data.length; i++) {
            data[i].showimage = "question-mark.png"
            data[i].shownom = "?"
            data[i].shownb = ""
            if(data[i].cat == "roi"){
              kings.push(data[i])
            }else{
              persos.push(data[i])
            }
          }
          this.setState({ rois: kings })
          this.setState({ personnages: persos })
        })
        .catch(console.log)

        
        fetch(baseURL+'evenement/start/400/end/600')
        .then(res => res.json())
        .then((data) => {
          for (var i = 0; i < data.length; i++) {
            if(data[i].startyear == data[i].endyear){
              data[i].showdate = data[i].startyear
            }else{
              data[i].showdate = data[i].startyear+" - "+data[i].endyear
            }
            data[i].showevt = "?"
            data[i].shownb = ""
          }
          this.setState({ evenements: data })
        })
        .catch(console.log)

        this.catchInstance = this.catchInstance.bind(this);
        this.catchInstance()
        
        this.setState({
          showBox1: true
        });
    
        setTimeout(() => {
            this.setState({
                showBox1: false
            });
          }, 5000);

    }

    handleClickShowAlert() {
      this.setState({
        showBox1: true
      });
    }

    handleClickShowMenu() {
      console.log("menu")
      this.setState({
        showMenu: true,
        showCharacter: false,
        showEvent: false,
        showKing: false,
        showMonument: false,
        showObject: false
      });
    }

    handleClickCloseMenu() {
      this.setState({
        showMenu: false,
        showThing: false
      });
    }
    
    handleClickCloseInfo() {
      this.setState({
        showBox1: false
      });
    }

    
    handleClickShowKing() {
      console.log("king")
      this.setState({
        showKing: true
      });
      this.setState({
        showMenu: false,
        showThing: true
      });
    }

    
    handleClickShowCharacter() {
      console.log("Character")
      this.setState({
        showCharacter: true
      });
      this.setState({
        showMenu: false,
        showThing: true
      });
    }

    
    handleClickShowMonument() {
      console.log("monument")
      this.setState({
        showMonument: true
      });
      this.setState({
        showMenu: false,
        showThing: true
      });
    }

    
    handleClickShowObject() {
      console.log("obj")
      this.setState({
        showObject: true
      });
      this.setState({
        showMenu: false,
        showThing: true
      });
    }
    
    handleClickShowEvent() {
      console.log("eve")
      this.setState({
        showEvent: true
      });
      this.setState({
        showMenu: false,
        showThing: true
      });
    }

    getInstances(id){
      let self = this;
      fetch(baseURL+'catch/user/1')
      .then(res => res.json())
      .then((data) => {
        self.state.personnages.forEach(function(personnage){
          if(personnage.id_personnage == id){
            self.setState({ ownInstance: data })
            console.log(personnage)
            self.setState({ headerMessage: "Félicitations ! Vous venez d'attraper : ", secondMessage: personnage.nom, urlImage: personnage.urlimage, isImage: true})
            self.handleClickShowAlert()
            self.forceUpdate()
          }
        });
        self.state.rois.forEach(function(personnage){
          if(personnage.id_personnage == id){
            self.setState({ ownInstance: data })
            self.setState({ headerMessage: "Félicitations ! Vous venez d'attraper : ", secondMessage: personnage.nom, urlImage: personnage.urlimage, isImage: true})
            self.handleClickShowAlert()
            self.forceUpdate()
          }
        });
        self.state.evenements.forEach(function(evenement){
          if(evenement.id_event == id){
            self.setState({ ownInstance: data })
            self.setState({ headerMessage: "Félicitations ! Vous venez d'attraper l'événement :", secondMessage: evenement.showdate+" - "+evenement.evenement, urlImage: "book.png",isImage: true})
            self.handleClickShowAlert()
            self.forceUpdate()
          }
        });
      })
      .catch(console.log)
    }


    catchInstance(id, type, lon, lat){
        let self = this;

        var tosend = {}
        tosend.id_external_object = id
        tosend.id_user = 1
        tosend.type_object = type
        tosend.lon = lon
        tosend.lat = lat
        console.log(id, type, lon, lat)
        console.log(JSON.stringify(tosend));

        if(id != undefined){

          gethttp().post(baseURL+"catch")
          .set('Content-Type', 'application/json')
          .send(JSON.stringify(tosend))
          .then(res => {
            if(res.status === 200){
              self.getInstances(tosend.id_external_object)
              
            } else {
              alert("Réponse " + res.statusCode + " : " + res.body);
            }
          })
          .catch(err =>{
            alert("Erreur lors de l'envoi des données au serveur : " + err.message);
          });
        }
    }

    componentDidUpdate() {
        let self = this;

        // add markers to map
        
        this.state.instances.forEach(function(marker){
            // create a HTML element for each feature
            var el = document.createElement('div');
            el.addEventListener('click', function() {
               self.catchInstance(marker.id_external_object, marker.type_object, marker.lon, marker.lat)
            });
            if(marker.type_object == "personnage"){ 
                el.className = 'marker-personnage';
            }
            if(marker.type_object == "evenement"){
                el.className = 'marker-evenement';
            }
        
            var coord = []
            coord[0] = marker.lon
            coord[1] = marker.lat

            new mapboxgl.Marker(el)
            .setLngLat(coord)
            .addTo(self.map);
        });
        

        self.state.personnages.forEach(function(personnage){
          count = 0
          self.state.ownInstance.forEach(function(instance){
            if(personnage.id_personnage == instance.id_external_object && instance.type_object == "personnage"){
              count = count + 1
            }
          });
          personnage.nb = count
          if(personnage.nb ==0){
            personnage.showimage = "question-mark.png"
            personnage.shownom = "?"
            personnage.shownb = ""
          }else{
            personnage.showimage = personnage.urlimage
            personnage.shownom = personnage.nom
            personnage.shownb = " (x"+personnage.nb+")"
          }
        });


        self.state.rois.forEach(function(personnage){
          count = 0
          self.state.ownInstance.forEach(function(instance){
            if(personnage.id_personnage == instance.id_external_object && instance.type_object == "personnage"){
              count = count + 1
            }
          });
          personnage.nb = count
          if(personnage.nb ==0){
            personnage.showimage = "question-mark.png"
            personnage.shownom = "?"
            personnage.shownb = ""
          }else{
            personnage.showimage = personnage.urlimage
            personnage.shownom = personnage.nom
            personnage.shownb = " (x"+personnage.nb+")"
          }
        });

        
        self.state.evenements.forEach(function(evenement){
          count = 0
          self.state.ownInstance.forEach(function(instance){
            if(evenement.id_event == instance.id_external_object && instance.type_object == "evenement"){
              count = count + 1
            }
          });
          evenement.nb = count
          if(evenement.nb ==0){
            evenement.showevt = "?"
            evenement.shownb = ""
          }else{
            evenement.showevt = evenement.evenement
            evenement.shownb = " (x"+evenement.nb+")"
          }
        });
    }
    
    componentDidMount() {

        this.map = new mapboxgl.Map({
            container: this.mapContainer,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [this.state.lng, this.state.lat],
            zoom: this.state.zoom
        });
         
        this.map.on('move', () => {
            this.setState({
                lng: this.map.getCenter().lng.toFixed(4),
                lat: this.map.getCenter().lat.toFixed(4),
                zoom: this.map.getZoom().toFixed(2)
            });
        });



    }


         
    render() {
        return (
          <div>
            <div>
            <div className={`sidebarStyle ${this.state.showBox1 ? 'alert-shown' : 'alert-hidden'}`}>
                <div style={{textAlign:"center"}}>
                  <h4>{this.state.headerMessage}</h4>
                  {this.state.isImage ? <span><img src={window.location.origin+"/images/kings/"+this.state.urlImage} width="40%"/></span> : <span>toto</span>}
                  <h5><i>{this.state.secondMessage}</i></h5>
                  <h5>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur tempor magna eget porta hendrerit. Nulla dignissim luctus tortor, in ultrices nulla varius a. Praesent sed ante neque. Vestibulum hendrerit eget leo eu sollicitudin. Sed metus risus, pellentesque eget ullamcorper ut, faucibus vel sapien. Nullam dui tellus, pretium pretium diam at, rhoncus commodo turpis.</h5>
                </div>
              </div>
              
              <div className={`menuButton infoButton ${this.state.showMenu ? 'alert-shown' : 'alert-hidden'}`}>
                <span onClick={this.handleClickCloseInfo.bind(this)}>
                  <img src={window.location.origin+"/images/error.png"} width="10%"  />
                </span>
              </div>

              <div className={`screenGray ${this.state.showMenu ? 'alert-shown' : 'alert-hidden'}`}>
                &nbsp;
              </div>
              <div className={`menuButton homeButton ${this.state.showMenu ? 'alert-hidden' : this.state.showThing ? 'alert-hidden' : 'alert-shown'}`}>
                <span onClick={this.handleClickShowMenu.bind(this)}>
                  <img src={window.location.origin+"/images/parchment.png"} width="15%"  />
                </span>
              </div>
              <div className={`menuButton homeButton ${this.state.showMenu ? 'alert-shown' : 'alert-hidden'}`}>
                <span onClick={this.handleClickCloseMenu.bind(this)}>
                  <img src={window.location.origin+"/images/error.png"} width="10%"  />
                </span>
              </div>
              <div className={`menuButton characterButton ${this.state.showMenu ? 'alert-shown' : 'alert-hidden'}`}>
                <span onClick={this.handleClickShowCharacter.bind(this)}>
                  <img src={window.location.origin+"/images/knight.png"} width="100%"/>
                </span>
              </div>
              <div className={`menuButton kingButton ${this.state.showMenu ? 'alert-shown' : 'alert-hidden'}`}>
                <span onClick={this.handleClickShowKing.bind(this)}>
                  <img src={window.location.origin+"/images/monarchy.png"} width="100%"/>
                </span>
              </div>
              <div className={`menuButton monumentButton ${this.state.showMenu ? 'alert-shown' : 'alert-hidden'}`}>
                <span onClick={this.handleClickShowMonument.bind(this)}>
                  <img src={window.location.origin+"/images/fortress.png"} width="100%"/>
                </span>
              </div>
              <div className={`menuButton objectButton ${this.state.showMenu ? 'alert-shown' : 'alert-hidden'}`}>
                <span onClick={this.handleClickShowObject.bind(this)}>
                  <img src={window.location.origin+"/images/chest.png"} width="100%"/>
                </span>
              </div>
              <div className={`menuButton eventButton ${this.state.showMenu ? 'alert-shown' : 'alert-hidden'}`}>
                <span onClick={this.handleClickShowEvent.bind(this)}>
                  <img src={window.location.origin+"/images/event.png"} width="100%"/>
                </span>
              </div>


              
              <div className={`kingPage ${this.state.showKing ? 'alert-shown' : 'alert-hidden'}`}>
                <span onClick={this.handleClickShowMenu.bind(this)}>
                  <img style={{margin: "3%"}} src={window.location.origin+"/images/previous.png"} width="10%"/>
                </span>
                <h3 style={{textAlign: "center", color: "white"}}>Votre KingDex</h3>
                {this.state.rois.map(personnage => (
                  <div className="vignette">
                      <img src={window.location.origin+"/images/kings/"+personnage.showimage} width="100px" height="100px"/>
                      <br/>
                      {personnage.shownom}{personnage.shownb}
                  </div>))}
              </div>
              <div className={`characterPage ${this.state.showCharacter ? 'alert-shown' : 'alert-hidden'}`}>
                <span onClick={this.handleClickShowMenu.bind(this)}>
                  <img style={{margin: "3%"}} src={window.location.origin+"/images/previous.png"} width="10%"/>
                </span>
                <h3 style={{textAlign: "center", color: "white"}}>Vos Persos</h3>
                {this.state.personnages.map(personnage => (
                  <div className="vignette">
                      <img src={window.location.origin+"/images/kings/"+personnage.showimage} width="100px" height="100px"/>
                      <br/>
                      {personnage.shownom}{personnage.shownb}
                  </div>))}



              </div>
              <div className={`monumentPage ${this.state.showMonument ? 'alert-shown' : 'alert-hidden'}`}>
                mon
              </div>
              <div className={`objectPage ${this.state.showObject ? 'alert-shown' : 'alert-hidden'}`}>
                obj
              </div>
              <div className={`eventPage ${this.state.showEvent ? 'alert-shown' : 'alert-hidden'}`}>
              <span onClick={this.handleClickShowMenu.bind(this)}>
                  <img style={{margin: "3%"}} src={window.location.origin+"/images/previous.png"} width="10%"/>
                </span>
                
                <div style={{height:"100%",textAlign:"center",color:"white", width:"100%", borderRadius:"10px"}}>
                      <h3>Frise Chrono</h3>
                      <Timeline lineColor={'#ddd'}>
                        {this.state.evenements.map(evenement => (
                          <TimelineItem
                            key="002"
                            dateText={evenement.showdate | 0}
                            dateInnerStyle={{ background: '#61b8ff', color: '#000' }}
                            bodyContainerStyle={{
                              background: '#ddd',
                              borderRadius: '8px',
                            }}
                          >
                            <h4 style={{ color: '#777777' }}>{evenement.showevt}</h4>
                          </TimelineItem>
                        ))}
                      </Timeline>
                    </div>


              </div>

              <div ref={el => this.mapContainer = el} className='mapContainer2' />
            </div>
          </div>
        )
    }
}

// Exporting the component 
export default MobilePageIndex; 
