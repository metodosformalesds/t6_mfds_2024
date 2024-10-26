import { React, useEffect } from "react";
import Layout from "../components/Layout";
import { Sidebar } from "../components/SideBar";
import Loans from "../components/Loans";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const { authData } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!authData.accessToken) {
      navigate("/login");
    }
  }, [authData, navigate]);

  return (
    <Layout isHome={false}>
      <div className="flex p-4">
        <Sidebar></Sidebar>
        <Loans />
      </div>
    </Layout>
  );
};

export default HomePage;
