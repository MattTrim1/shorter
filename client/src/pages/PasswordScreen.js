import { useState } from "react";
import { auth } from "../services/UrlService";

function PasswordScreen(props) {
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Make API call to ensure our password is correct
    const authed = auth(password);
    (authed === true) ? props.setIsAuthed(authed) : alert("Unable to authenticate.");
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>Enter the password:
          <input 
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)} 
          />
          <input type="submit" value={"Submit"} />
        </label>
      </form>
    </div>
  );
}

export default PasswordScreen;