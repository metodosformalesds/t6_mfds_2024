import React from "react";
import { useEffect } from "react"; 
import Layout from "../components/Layout";
import { CarouselDefault } from "../components/LandingPage/Carousell";
import { ContentDesign } from "../components/LandingPage/Content";
import { initLandbot } from "../components/bot/bot";
const LandingPage = () => {
  useEffect(() => {
    initLandbot();
  }, []);  
  return (
    <Layout>
    <CarouselDefault></CarouselDefault>
    <ContentDesign></ContentDesign>
    </Layout>
  );

};

export default LandingPage;
