import React from 'react';
import ReactDOM from 'react-dom';
import './css/index.css';
import App from './components/App';
import { getFullUrl } from './services/UrlService';

const path = document.location.pathname.toString();

if (path !== '/') {
  getFullUrl(path.substring(1))
  .then(r => {
    console.log(r);
    window.location.replace(r.data.full_url);
  })
  .catch(e => {
    alert('Could not resolve full URL from shortcode.')
    console.log(e);
  });
}
else {
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    document.getElementById('root')
  );  
}