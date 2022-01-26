import { useState } from "react";
import { auth } from "../services/UrlService";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

function PasswordScreen(props) {
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Make API call to ensure our password is correct
    auth(password)
      .then((r) => {
        (r['status'] === 200) ? props.setIsAuthed(true) : props.setIsAuthed(false); // TODO: Remove the 'then' call
      })
      .catch((e) => {
        console.log(e);
        alert("Unable to authenticate.");
      });
  }

  return (
    <div>
      <Form onSubmit={handleSubmit} className="text-center mt-3">
        <Form.Group className="mb-3" controlId="formBasicAuth">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Enter password" onChange={(e) => setPassword(e.target.value)} />
        </Form.Group>
        <Button variant="info" type="submit">Submit</Button>
      </Form>
    </div>
  );
}

export default PasswordScreen;