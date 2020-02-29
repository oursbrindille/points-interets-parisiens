import React, {Component} from 'react'; 
import ReactDOM from 'react-dom';
import mapboxgl from 'mapbox-gl';

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
        lng: 2.3367,
        lat: 48.8608,
        zoom: 11.5,
        instances:[],
        ownInstance:[],
        rois:[],
        headerMessage:""
    };


        fetch('http://localhost:5001/generate')
        .then(res => res.json())
        .then((data) => {
          this.setState({ instances: data })
        })
        .catch(console.log)

        
        fetch('http://localhost:5000/instance-user/user/1')
        .then(res => res.json())
        .then((data) => {
          this.setState({ ownInstance: data })
        })
        .catch(console.log)

        
        fetch('http://localhost:5000/roi/start/500/end/600')
        .then(res => res.json())
        .then((data) => {
          this.setState({ rois: data })
        })
        .catch(console.log)

        this.catchInstance = this.catchInstance.bind(this);
        this.catchInstance()
    }

    getInstances(id){
      let self = this;
      fetch('http://localhost:5000/instance-user/user/1')
      .then(res => res.json())
      .then((data) => {
        self.state.rois.forEach(function(roi){
          console.log(roi.id_roi);
          if(roi.id_roi == id){
            self.setState({ ownInstance: data })
            self.setState({ headerMessage: "Félicitations ! Vous venez d'attraper "+roi.nom})
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

          gethttp().post("http://localhost:5000/instance-user")
          .set('Content-Type', 'application/json')
          .send(JSON.stringify(tosend))
          .then(res => {
            if(res.status === 200){
              console.log("valou", tosend);
              self.getInstances(tosend.id_external_object)
              
            } else {
              alert("Réponse " + res.statusCode + " : " + res.body);
            }
          })
          .catch(err =>{
            console.log("fail");
            alert("Erreur lors de l'envoi des données au serveur : " + err.message);
          });
        }
    }

    componentDidUpdate() {
        let self = this;

        console.log('mounted or updated');
        // add markers to map
        
        this.state.instances.forEach(function(marker){
            // create a HTML element for each feature
            var el = document.createElement('div');
            el.addEventListener('click', function() {
               self.catchInstance(marker.id_external_object, marker.type_object, marker.lon, marker.lat)
            });
            if(marker.type_object == "roi"){ 
                el.className = 'marker-roi';
            }
            if(marker.type_object == "evenement"){
                el.className = 'marker-evenement';
            }
            if(marker.type_object == "personnage"){
                el.className = 'marker-personnage';
            }
        
            var coord = []
            coord[0] = marker.lon
            coord[1] = marker.lat

            new mapboxgl.Marker(el)
            .setLngLat(coord)
            .addTo(self.map);
        });
        

        self.state.rois.forEach(function(roi){
          count = 0
          self.state.ownInstance.forEach(function(instance){
            if(roi.id_roi == instance.id_external_object){
              count = count + 1
            }
          });
          roi.nb = count
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

        console.log(this.state.instances)


    }


         
    render() {
        return (
            <div style={{float:"left", width:"100%", height:"100%", margin:"50px"}}>
                <div style={{float:"left", width:"45%"}}>
                  <div className='sidebarStyle'>
                      <div>Longitude: {this.state.lng} | Latitude: {this.state.lat} | Zoom: {this.state.zoom}</div>
                      </div>
                  <div ref={el => this.mapContainer = el} className='mapContainer' />
                </div>
                <div style={{float:"left", width:"55%"}}>
                  <div><h2>{this.state.headerMessage}</h2></div>
                  <div>{this.state.rois.map(roi => (<div>{roi.nom} - {roi.nb}</div>))}</div>
                </div>
            </div>
        )
    }
}

// Exporting the component 
export default MapPage; 
