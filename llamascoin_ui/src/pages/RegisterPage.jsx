import React, { useEffect } from "react";
import Layout from "../components/Layout";
import { MultiStepForm } from "../components/RegisterForm/MultiStepForm";
const RegisterPage = () => {


  return (
    <Layout>
        <MultiStepForm></MultiStepForm>
    </Layout>
  );
};

export default RegisterPage;
