import React, { useState } from "react";
import axios from "axios";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://localhost:8000/token", {
        username,
        password,
      });
      setToken(response.data.access_token);
    } catch (error) {
      console.error("Login failed", error);
    }
  };

  const handleProtectedRequest = async () => {
    try {
      const response = await axios.get("http://localhost:8000/users/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log("Protected data", response.data);
    } catch (error) {
      console.error("Protected request failed", error);
    }
  };

  return (
    <div className="App">
      <h1>Login System</h1>
      <div>
        <label>Username:</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <button onClick={handleLogin}>Login</button>
      {token && (
        <div>
          <h2>Token:</h2>
          <p>{token}</p>
          <button onClick={handleProtectedRequest}>
            Make Protected Request
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
