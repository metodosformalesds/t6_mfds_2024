import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import LandingPage from "./pages/LandingPage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import Subscription from "./pages/Subscription";

const App = () => {
  return (
    <Router>
  
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage/>}/>
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/subscription" element={<Subscription />} />
        </Routes>
    </Router>
  );
};

export default App;