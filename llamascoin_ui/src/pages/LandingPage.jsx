import React from "react";
import Layout from "../components/Layout";

const LandingPage = () => {
  return (
    <Layout>
      <h1 className="text-3xl font-bold ">
      Hello world!
    </h1>
      <p>
        This is the homepage where you can find various resources and information.
        Explore our content and feel free to reach out if you have any questions.
      </p>
      
      <button onClick={() => alert("Button clicked!")}>Get Started</button>
    </Layout>
  );
};

export default LandingPage;
