import React, { useEffect, useState } from "react";
import Layout from "../components/Layout";
import { Sidebar } from "../components/SideBar";
import Loans from "../components/Loans";
import MoneylenderDashboard from "../components/MoneylenderDashboard";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import CreditHistory from "../components/CreditHistory";

const HomePage = () => {
  const { authData } = useAuth();
  const navigate = useNavigate();
  const role = authData?.role;

  const [activeComponent, setActiveComponent] = useState(null);

  useEffect(() => {
    if (!authData.accessToken || !role) {
      navigate("/login");
    } else {
      setActiveComponent(role === "borrower" ? "loans" : "dashboard");
    }
  }, [authData, role, navigate]);

  const renderComponent = () => {
    switch (activeComponent) {
      case 'loans':
        return <Loans />;
      case 'dashboard':
        return <MoneylenderDashboard />;
      case 'creditHistory':
        return <CreditHistory/>; 
      case 'fees':
        return <div>Suscripción</div>; 
      case 'account':
        return <div>Cuenta</div>; e
      default:
        return null;
    }
  };

  return (
    <Layout isHome={false}>
      <div className="flex p-4">
        <Sidebar onSelect={setActiveComponent} />
        {renderComponent()}
      </div>
    </Layout>
  );
};

export default HomePage;
