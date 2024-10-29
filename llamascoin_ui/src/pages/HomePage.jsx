import React, { useEffect } from "react";
import Layout from "../components/Layout";
import { Sidebar } from "../components/SideBar";
import Loans from "../components/Loans";
import MoneylenderDashboard from "../components/MoneylenderDashboard";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const { authData } = useAuth();
  const navigate = useNavigate();
  const role = authData?.role;

  useEffect(() => {
    if (!authData.accessToken || !role) {
      navigate("/login");
    }
  }, [authData, role, navigate]);

  if (role === "borrower") {
    return (
      <Layout isHome={false}>
        <div className="flex p-4">
          <Sidebar />
          <Loans />
        </div>
      </Layout>
    );
  } else if (role === "moneylender") {
    return (
      <Layout isHome={false}>
        <div className="flex p-4">
          <Sidebar />
          <MoneylenderDashboard/>
        </div>
      </Layout>
    );
  }
  return null;
};

export default HomePage;
