import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import 'typeface-roboto'; // Import Roboto
import 'typeface-roboto-condensed'; // Import Roboto Condensed
import 'typeface-roboto-slab'; // Import Roboto Slab
import 'typeface-poppins';
import 'typeface-courier-prime';
import 'typeface-exo';
import 'typeface-lora';
import 'typeface-barlow';
import 'typeface-open-sans';
import 'typeface-lato';
import 'typeface-merriweather';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
