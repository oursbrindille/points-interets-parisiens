import React, {Component} from 'react'; 
import ReactDOM from 'react-dom';
import mapboxgl from 'mapbox-gl';

mapboxgl.accessToken = 'pk.eyJ1Ijoic2Fib3N0aXgiLCJhIjoiY2p6Y3BkdnJ4MDd2czNjbWdsYXB4MTJoNSJ9.U65hBBejoDAAJH5wrdLejg';

var geojson = {
    type: 'FeatureCollection',
    features: [{
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [2.40167, 48.858983]
      },
      properties: {
        title: 'Mapbox',
        description: 'Washington, D.C.'
      }
    },
    {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [-122.414, 37.776]
      },
      properties: {
        title: 'Mapbox',
        description: 'San Francisco, California'
      }
    }]
  };
  
class MapPage extends Component { 
    
    constructor(props) {
        super(props);
        this.state = {
        lng: 2.3367,
        lat: 48.8608,
        zoom: 11.5,
        instances:[],
        ownInstance:[],
        toto:""
        };


        fetch('http://localhost:5001/generate')
        .then(res => res.json())
        .then((data) => {
          this.setState({ instances: data })
        })
        .catch(console.log)

        this.catchInstance = this.catchInstance.bind(this);
    }

    catchInstance(){
        this.state.toto = 'oooo'
        console.log("ooooo")
    }

    componentDidUpdate() {
        let self = this;

        console.log('mounted or updated');
        // add markers to map
        
        this.state.instances.forEach(function(marker){
            // create a HTML element for each feature
            var el = document.createElement('div');
            el.addEventListener('click', function() {
               self.catchInstance()
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
            .setPopup(new mapboxgl.Popup({ offset: 25 }) // add popups
              .setHTML('<p>' + marker.id_external_object + '</p>'))
            .addTo(self.map);
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
            <div>
                <div className='sidebarStyle'>
                    <div>Longitude: {this.state.lng} | Latitude: {this.state.lat} | Zoom: {this.state.zoom}</div>
                    </div>
                <div ref={el => this.mapContainer = el} className='mapContainer' />
            </div>
        )
    }
}

// Exporting the component 
export default MapPage; 
