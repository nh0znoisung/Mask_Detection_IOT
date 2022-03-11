// npm install react-bootstrap bootstrap@5.1.3 react-router-dom@6 axios video-react react react-dom redux firebase --save

import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import {BrowserRouter} from 'react-router-dom';

ReactDOM.render(
  <BrowserRouter>
     <App />
  </BrowserRouter>
  ,document.getElementById('root')
);


