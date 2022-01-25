const axios = require('axios').default;

async function auth(password) {
  return await axios.post(`${process.env.REACT_APP_API_URL}/v1/auth`, {
    "password": password
  });
};

async function shortenUrl(longUrl, shortcode = null) {
  const req = {
    "full_url": longUrl,
    ...(shortcode !== null && {"shortcode": shortcode})
  };

  return await axios.post(`${process.env.REACT_APP_API_URL}/v1/url`, req);
}

function getFullUrl(shortcode) {
  // TODO: Implement
}

function isValidUrl(value) {
  const expression = /http[s]?:\/\/[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
  const regexp = new RegExp(expression);
  return regexp.test(value);
}

export { auth, shortenUrl, getFullUrl, isValidUrl };