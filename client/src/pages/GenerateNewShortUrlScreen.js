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
      .then(r => handleApiResponse(r))
      .catch(e => {
        console.log(e);
        alert("Unable to shorten URL.");
        resetFormInputField();
      });
  }

  const handleApiResponse = (response) => {
    resetFormInputField();
    const data = response.data;
    if (data.status === "success") {
      setSuccess(true);
      setShowForm(false);
      setShortcode(data.shortcode);
      setExpiry(data.expires_at);
    }
    else {
      alert("Unable to shorten URL.");
      resetFormInputField();
    }
  }

  const resetState = (e) => {
    e.preventDefault();

    setUrl("");
    setSuccess(false);
    setShowForm(true);
    setShortcode("");
    setExpiry("");
  }

  const resetFormInputField = () => {
    document.getElementById("formSubmitLongURL").value = "";
  }

  const generateShortUrl = () => {
    return `${window.location.href}${shortcode}`;
  }

  return (
    <section className="text-center">
      <h3 className="mb-3">Welcome!</h3>
      {success ? (
        <>
          <h3>Success</h3>
          <p>Your short URL is: <a href={generateShortUrl()}>{generateShortUrl()}</a>.</p>
          <p>It expires on {expiry}!</p>
          <Button variant="info" type="submit" onClick={resetState}>Create New</Button>
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