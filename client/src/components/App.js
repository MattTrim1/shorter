import { useState } from "react";
import PasswordScreen from "../pages/PasswordScreen";
import GenerateNewShortUrlScreen from "../pages/GenerateNewShortUrlScreen";
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [isAuthed, setIsAuthed] = useState(false);

  return (
    <div className="container">
      <h1>shorter.</h1>
        {isAuthed ? <GenerateNewShortUrlScreen /> : <PasswordScreen setIsAuthed={setIsAuthed} />}
      </div>
  );
}

export default App;