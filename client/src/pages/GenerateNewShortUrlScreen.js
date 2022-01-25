import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { shortenUrl, isValidUrl } from "../services/UrlService";

function GenerateNewShortUrlScreen() {
  const [url, setUrl] = useState("");
  const [success, setSuccess] = useState(false);
  const [showForm, setShowForm] = useState(true);
  const [shortcode, setShortcode] = useState("");
  const [expiry, setExpiry] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // validate we have a good URL
    const valid = isValidUrl(url);

    // attempt to shorten the URL 
    if (!valid) {
      alert("Invalid URL.");
      resetFormInputField();
      return;
    }

    shortenUrl(url)
      .then(r => handleResponse(r))
      .catch(e => {
        console.log(e);
        alert("Unable to shorten URL.");
        resetFormInputField();
      });
  }

  const handleResponse = (response) => {
    // check our response is valid
    // if created, display the newly created URL
    resetFormInputField();
    console.log(response);
    const data = response.data;
    setSuccess(true);
    setShowForm(false);
    setShortcode(data.shortcode);
    setExpiry(data.expires_at);
  }

  const resetFormInputField = () => {
    document.getElementById("formSubmitLongURL").value = "";
  }

  return (
    <section className="text-center">
      <h3 className="mb-3">Welcome!</h3>
      {success ? (
        <>
          <h3>Success</h3>
          <p>Your short URL is: {window.location.href}{shortcode}.</p>
          <p>It expires on {expiry}!</p>
        </>
      ) : <></>}
      {showForm && (
        <Form onSubmit={handleSubmit} className="mt-3">
          <Form.Group className="mb-3" controlId="formSubmitLongURL">
            <Form.Label>URL to shorten</Form.Label>
            <Form.Control type="text" placeholder="Enter URL" onChange={(e) => setUrl(e.target.value)} />
          </Form.Group>
          <Button variant="info" type="submit">Submit</Button>
        </Form>
      )}
    </section>
  );
}

export default GenerateNewShortUrlScreen;