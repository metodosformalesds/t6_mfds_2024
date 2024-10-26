// src/pages/LoginPage.js
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import { LoginForm } from "../components/LoginForm";
import { useAuth } from "../context/AuthContext"; 

const LoginPage = () => {
  const { authData } = useAuth(); 
  const navigate = useNavigate(); 

  useEffect(() => {
    if (authData.accessToken) {
      navigate('/home'); 
    }
  }, [authData, navigate]);

  return (
    <Layout>
      <LoginForm />
    </Layout>
  );
};

export default LoginPage;
