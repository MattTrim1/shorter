import { useState } from "react";
import PasswordScreen from "../pages/PasswordScreen";
import GenerateNewShortUrlScreen from "../pages/GenerateNewShortUrlScreen";

function App() {
  const [isAuthed, setIsAuthed] = useState(false);

  return (
    <div>
      <h1>shorter.</h1>
        {isAuthed ? <GenerateNewShortUrlScreen /> : <PasswordScreen setIsAuthed={setIsAuthed} />}
      </div>
  );
}

export default App;