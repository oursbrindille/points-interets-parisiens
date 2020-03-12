import React, {Component} from 'react'; 
import ReactDOM from 'react-dom';
import mapboxgl from 'mapbox-gl';
import { Timeline, TimelineItem }  from 'vertical-timeline-component-for-react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';


mapboxgl.accessToken = 'pk.eyJ1Ijoic2Fib3N0aXgiLCJhIjoiY2p6Y3BkdnJ4MDd2czNjbWdsYXB4MTJoNSJ9.U65hBBejoDAAJH5wrdLejg';

var count = 0
var baseURL = "http://localhost:5000/"

export function gethttp(){
  var http = require('superagent');
  return http;
}

class MobilePageIndex extends Component { 
    
    constructor(props) {
        super(props);
        this.state = {
        lng: 2.3038,
        lat: 48.8422,
        zoom: 14.5,
        instances:[],
        ownInstance:[],
        rois:[],
        personnages:[],
        evenements:[],
        headerMessage:"MerovinGo!",
        secondMessage:"Observer aux alentours, et tenter d'attraper de la connaissance!",
        baseImageUrl:"../images/kings/",
        showBox1: false
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
        


    }

    handleClickShowAlert() {
        let self = this;

        console.log("clik")
        this.setState({
          showBox1: true
        });
    
        setTimeout(() => {
            this.setState({
                showBox1: false
            });
          }, 2000);


          var el = document.createElement('div');

          el.className = 'marker-personnage';
          
          var coord = []
          coord[0] = 2.3038
          coord[1] = 48.8422

          new mapboxgl.Marker(el)
          .setLngLat(coord)
          .addTo(self.map);
      }

    getInstances(id){
      let self = this;
      fetch(baseURL+'catch/user/1')
      .then(res => res.json())
      .then((data) => {
        self.state.personnages.forEach(function(personnage){
          if(personnage.id_personnage == id){
            self.setState({ ownInstance: data })
            self.setState({ headerMessage: "Félicitations ! Vous venez d'attraper : ", secondMessage: personnage.nom})
            self.forceUpdate()
          }
        });
        self.state.rois.forEach(function(personnage){
          if(personnage.id_personnage == id){
            self.setState({ ownInstance: data })
            self.setState({ headerMessage: "Félicitations ! Vous venez d'attraper : ", secondMessage: personnage.nom})
            self.forceUpdate()
          }
        });
        self.state.evenements.forEach(function(evenement){
          if(evenement.id_event == id){
            self.setState({ ownInstance: data })
            self.setState({ headerMessage: "Félicitations ! Vous venez d'attraper l'événement :", secondMessage: evenement.showdate+" - "+evenement.evenement})
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
              <div className='sidebarStyle'>
                <div style={{textAlign:"center"}}>
                  <h4>{this.state.headerMessage}</h4><h5><i>{this.state.secondMessage}</i></h5>
                  <button onClick={this.handleClickShowAlert.bind(this)}>
                    Show alert
                  </button>
                  {this.state.instances.map(instance => (<p>{instance.id_external_object}</p>))}
                </div>
              </div>
              <div className={`alert alert-success ${this.state.showBox1 ? 'alert-shown' : 'alert-hidden'}`}>
                    <strong>Success!</strong> Thank you for subscribing!
            </div>
              <div ref={el => this.mapContainer = el} className='mapContainer2' />
            </div>

          </div>
        )
    }
}

// Exporting the component 
export default MobilePageIndex; 
