import React from "react";
import { Routes, Route } from "react-router";

import Signin from "./Pages/Signin";
import Signup from "./Pages/Signup";
import Chatbot from "./Pages/Chatbot";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Signup />} />
      <Route path="signin" element={<Signin />} />
      <Route path="chatbot" element={<Chatbot />} />
    </Routes>
  );
}

export default App;
