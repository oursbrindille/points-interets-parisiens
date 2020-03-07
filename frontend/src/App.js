import React from 'react';
import logo from './logo.svg';
import './App.css';
import './css/site.css';
import ParisPage from './components/parisPage.jsx'
import { BrowserRouter, Route, Switch } from "react-router-dom";
import MapPage from './components/mapPage';


function App() {
  return (
     <BrowserRouter>
        <div>
          <Switch>
            <Route path="/" component={ParisPage} exact />
            <Route path="/map" component={MapPage} />
          </Switch>
        </div>
      </BrowserRouter>
  );
}

export default App;


