import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import Stepper from "./Stepper";
import { Step1 } from "./Step1";
import { Step2 } from "./Step2";
import { Step3 } from "./Step3";
import { Step4 } from "./Step4";
import { Button, Typography } from "@material-tailwind/react";
import { useNavigate } from "react-router-dom";
import StatusComponent from "../StatusComponent";
import axios from "axios";
import { apiHost, validationForm } from "../../utils/apiconfig";
import { useAuth } from "../../context/AuthContext";

export function MultiStepForm() {
  const [status, setStatus] = useState("");
  const navigate = useNavigate();
  const { authData } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors },
    getValues,
    trigger,
    setValue,
  } = useForm({
    defaultValues: {
      account_type: "",
      email: "",
      password: "",
      paypal_email: "",
      curp: "",
    },
  });

  useEffect(() => {
    if (authData.accessToken) {
      navigate("/home");
    }
  }, [authData, navigate]);

  const [step, setStep] = useState(0);

  const onSubmit = async () => {
    const result = await trigger();
    if (result){
      const formData = getValues();

    const { email, password, account_type, paypal_email, curp } = formData;

    const dataToSubmit = {
      email,
      password,
      account_type,
      paypal_email,
      curp,
    };

    try {
      setStatus("loading");
      const response = await axios.post(apiHost + "register/", dataToSubmit, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.status === 201) {
        setStatus("success");
        setStep((currentStep) => currentStep + 1);
        setStatus("");
      } else {
        setStatus("error");
      }
    } catch (error) {
      console.error("Error al registrar:", error);
      setStatus("error");
    }
    }
    
  };

  const nextStep = async () => {
    const result = await trigger();
    if (result) {
    if(status ==="sucess"){
      setStatus("")
    }

    setStep((currentStep) => currentStep + 1);
    }
  };

  const prevStep = () => {
    setStatus("")
    setStep((currentStep) => currentStep - 1);
  };

  function getStepContent(step) {
    switch (step) {
      case 0:
        return <Step1 register={register} errors={errors} />;
      case 1:
        return <Step2 register={register} errors={errors} />;
      case 2:
        return <Step3 register={register} errors={errors} />;
      case 3:
        return <Step4 />;
      default:
        return "No hay paso definido";
    }
  }

  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <div className="flex flex-col justify-between sm:mx-auto sm:w-full min-h-[500px] sm:max-w-md sm:px-10 p-5 shadow-lg rounded-lg">
        <div>
          <Typography variant="h3" className="font-bold">
            Crear cuenta
          </Typography>
          <Stepper currentStep={step} />

          {status === "loading" || status === "error" || status === "success" ? (
            <StatusComponent status={status} />
          ) : (
            <form>{getStepContent(step)}</form>
          )}
        </div>

        <div className="mt-6 flex justify-between">
          {step === 0 && (
            <Button
              color="blue"
              variant="filled"
              onClick={nextStep}
              className="ml-auto"
              disabled={status === "loading"}
            >
              Siguiente
            </Button>
          )}
          {step === 1 && (
            <>
              <Button
                color="blue"
                variant="outlined"
                onClick={prevStep}
                className="mr-2"
                disabled={status === "loading"}
              >
                Anterior
              </Button>
              <Button
                onClick={handleSubmit(onSubmit)}
                color="green"
                variant="filled"
                className="ml-auto"
                disabled={status === "loading"}
              >
                Enviar
              </Button>
            </>
          )}
          {step === 2 && (
            <Button
              onClick={() => {
                window.open(validationForm, "_blank");
                nextStep();
              }}
              color="green"
              variant="filled"
              className="m-auto"
            >
              Validar identidad
            </Button>
          )}
          {step === 3 && null}
        </div>
      </div>
    </div>
  );
}
