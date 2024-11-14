import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import LandingPage from "./pages/LandingPage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import TermsAndConditions from "./pages/TermsAndConditions";
import HomePage from "./pages/HomePage";
import { AuthProvider } from "./context/AuthContext";
import AboutUs from "./pages/AboutUs";
import FeesPage from "./pages/FeesPage";
const App = () => {
  return (
    <AuthProvider> 
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/fees" element={<FeesPage />} />
        <Route path="/terms-and-conditions" element={<TermsAndConditions />} />
        <Route path="/about" element={<AboutUs/>}/>

      </Routes>
    </Router>
  </AuthProvider>
  );
};

export default App;