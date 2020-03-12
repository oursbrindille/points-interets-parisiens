import React from 'react';
import logo from './logo.svg';
import './App.css';
import './css/site.css';
import ParisPage from './components/parisPage.jsx'
import { BrowserRouter, Route, Switch } from "react-router-dom";
import MapPage from './components/mapPage';
import MobilePageIndex from './components/mobilePageIndex';


function App() {
  return (
     <BrowserRouter>
        <div>
          <Switch>
            <Route path="/" component={MapPage} exact />
            <Route path="/mobile" component={MobilePageIndex} exact />
          </Switch>
        </div>
      </BrowserRouter>
  );
}

export default App;


