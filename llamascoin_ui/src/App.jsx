import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import LandingPage from "./pages/LandingPage";

const App = () => {
  return (
    <Router>
  
        <Routes>
          <Route path="/" element={<LandingPage />} />
         
        </Routes>
  
    </Router>
  );
};

export default App;