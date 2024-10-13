import React from "react";
import Layout from "../components/Layout";
import { CarouselDefault } from "../components/LandingPage/Carousell";
import { ContentDesign } from "../components/LandingPage/Content";
const LandingPage = () => {
  return (
    <Layout>
    <CarouselDefault></CarouselDefault>
    <ContentDesign></ContentDesign>
    </Layout>
  );

};

export default LandingPage;
