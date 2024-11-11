import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import LandingPage from "./pages/LandingPage";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import Subscription from "./pages/Subscription";
import TermsAndConditions from "./pages/TermsAndConditions";
import HomePage from "./pages/HomePage";
import { AuthProvider } from "./context/AuthContext";
import AboutUs from "./pages/AboutUs";
import Calendar from "./components/calendar"
const App = () => {
  return (
    <AuthProvider> 
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/subscription" element={<Subscription />} />
        <Route path="/terms-and-conditions" element={<TermsAndConditions />} />
        <Route path="/about" element={<AboutUs/>}/>
        <Route path="/calendar" element={<Calendar/>}/>
      </Routes>
    </Router>
  </AuthProvider>
  );
};

export default App;