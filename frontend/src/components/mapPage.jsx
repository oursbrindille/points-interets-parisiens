import React, {Component} from 'react'; 
import ReactDOM from 'react-dom';
import mapboxgl from 'mapbox-gl';
import { Timeline, TimelineItem }  from 'vertical-timeline-component-for-react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';


mapboxgl.accessToken = 'pk.eyJ1Ijoic2Fib3N0aXgiLCJhIjoiY2p6Y3BkdnJ4MDd2czNjbWdsYXB4MTJoNSJ9.U65hBBejoDAAJH5wrdLejg';

var count = 0

export function gethttp(){
  var http = require('superagent');
  return http;
}

class MapPage extends Component { 
    
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
        baseImageUrl:"../images/kings/"
    };


        fetch('http://localhost:5000/instances/generate')
        .then(res => res.json())
        .then((data) => {
          this.setState({ instances: data })
        })
        .catch(console.log)

        
        fetch('http://localhost:5000/catch/user/1')
        .then(res => res.json())
        .then((data) => {
          this.setState({ ownInstance: data })
        })
        .catch(console.log)

        
        fetch('http://localhost:5000/personnage/start/400/end/600')
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

        
        fetch('http://localhost:5000/evenement/start/400/end/600')
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

    getInstances(id){
      let self = this;
      fetch('http://localhost:5000/catch/user/1')
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

          gethttp().post("http://localhost:5000/catch")
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
            <div style={{margin:"20px"}}>
              <div className='sidebarStyle'>
                <div style={{width:"385px",textAlign:"center"}}>
                  <h4>{this.state.headerMessage}</h4><h5><i>{this.state.secondMessage}</i></h5>
                </div>
              </div>
              <div ref={el => this.mapContainer = el} className='mapContainer' />
            </div>


            <div style={{float:"left", width:"100%", height:"100%"}}>
                <div style={{float:"left", width:"25%"}}>
                  &nbsp;
                </div>
                <div style={{float:"left", width:"70%", marginLeft:"20px"}}>

                <Tabs>
                  <TabList>
                    <Tab>KingDEX</Tab>
                    <Tab>Frise Chrono</Tab>
                    <Tab>Vos Persos</Tab>
                  </TabList>

                  <TabPanel>
                    <div style={{float:"left", height:"100%",textAlign:"center",color:"white", backgroundColor:"#12556B", borderRadius:"10px"}}>
                      <h3>Votre KingDex</h3>
                      {this.state.rois.map(personnage => (
                        <div style={{margin:"20px",textAlign:"center",float:"left", height:"100%"}}>
                            <img src={window.location.origin+"/images/kings/"+personnage.showimage} width="100px" height="100px"/>
                            <br/>
                            {personnage.shownom}{personnage.shownb}
                        </div>))}
                    </div>
                  </TabPanel>
                  <TabPanel>
                    <div style={{float:"left", height:"100%",textAlign:"center",color:"white", width:"100%", backgroundColor:"#12556B", marginTop:"20px", borderRadius:"10px"}}>
                      <h3>Frise Chrono</h3>
                      <Timeline lineColor={'#ddd'}>
                        {this.state.evenements.map(evenement => (
                          <TimelineItem
                            key="002"
                            dateText={evenement.showdate | 0}
                            dateInnerStyle={{ background: '#61b8ff', color: '#000' }}
                            bodyContainerStyle={{
                              background: '#ddd',
                              padding: '10px',
                              borderRadius: '8px',
                              boxShadow: '0.5rem 0.5rem 2rem 0 rgba(0, 0, 0, 0.2)',
                            }}
                          >
                            <h4 style={{ color: '#777777' }}>{evenement.showevt}</h4>
                          </TimelineItem>
                        ))}
                      </Timeline>
                    </div>
                  </TabPanel>
                  <TabPanel>
                    <div style={{float:"left", height:"100%",textAlign:"center",color:"white", backgroundColor:"#12556B", borderRadius:"10px"}}>
                        <h3>Vos Persos</h3>
                        {this.state.personnages.map(personnage => (
                          <div style={{margin:"20px",textAlign:"center",float:"left", height:"100%"}}>
                              <img src={window.location.origin+"/images/kings/"+personnage.showimage} width="100px" height="100px"/>
                              <br/>
                              {personnage.shownom}{personnage.shownb}
                          </div>))}
                      </div>
                  </TabPanel>
                </Tabs>


                </div>
            </div>
          </div>
        )
    }
}

// Exporting the component 
export default MapPage; 
