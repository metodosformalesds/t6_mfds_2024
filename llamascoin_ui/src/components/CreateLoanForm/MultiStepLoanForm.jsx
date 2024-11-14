import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import Stepper from "./Stepper";
import { Step1 } from "./Step1";
import { Step2 } from "./Step2";
import { Button, Typography } from "@material-tailwind/react";
import { useNavigate } from "react-router-dom";
import StatusComponent from "../StatusComponent";
import { apiHost } from "../../utils/apiconfig";
import { useAuth } from "../../context/AuthContext";
import { useFetch } from "../../hooks/useFetch";
import axios from "axios";

export function MultiStepLoanForm() {
  const { authData } = useAuth();
  const navigate = useNavigate();

  const { status: userStatus, data } = useFetch(
    apiHost + "user/" + authData.userId
  );

  const {
    register,
    handleSubmit,
    formState: { errors },
    trigger,
    getValues,
  } = useForm({
    defaultValues: {
      amount: 0,
      term: "1",
      interest_rate: 0,
      number_of_payments: 0
    },
  });

  const [step, setStep] = useState(0);
  const [loanStatus, setLoanStatus] = useState("");

  useEffect(() => {
    if (userStatus === "success") {
      setLoanStatus("success");
    } else if (userStatus === "error") {
      setLoanStatus("error");
    }
  }, [userStatus]);

  const onSubmit = async () => {
    const formData = getValues();
    const { amount, term, interest_rate, number_of_payments } = formData;

    const dataToSubmit = {
      amount,
      term,
      interest_rate,
      number_of_payments,
    };

    setLoanStatus("loading");
    try {
      const response = await axios.post(`${apiHost}loan/`, dataToSubmit, {
        headers: {
          Authorization: `Bearer ${authData.accessToken}`, // Si necesitas el token de autorización
          "Content-Type": "application/json",
        },
      });

      setLoanStatus("success");
      console.log("Loan exitosa:", response.data);
      navigate(0);
    } catch (error) {
      console.error(
        "Error en el registro:",
        error.response?.data || error.message
      );
      setLoanStatus("error");
    }
  };

  const nextStep = async () => {
    const result = await trigger();
    if (result) {
      setStep((currentStep) => currentStep + 1);
    }
  };

  const prevStep = () => {
    setStep((currentStep) => currentStep - 1);
  };

  function getStepContent(step) {
    switch (step) {
      case 0:
        return (
          <Step1
            register={register}
            errors={errors}

          />
        );
      case 1:
        return <Step2 register={register} errors={errors} getValues ={getValues} />;
      default:
        return "No hay paso definido";
    }
  }

  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <div className="flex flex-col justify-between sm:mx-auto sm:w-full min-h-[500px] sm:max-w-md sm:px-10 p-5 shadow-lg rounded-lg">
        <div>
          <Typography variant="h3" className="font-bold">
            Publicar préstamo
          </Typography>
          <Stepper currentStep={step} />

          {loanStatus === "loading" ? (
            <StatusComponent status="loading" />
          ) : loanStatus === "error" && step > 1 ? (
            <StatusComponent status="error" />
          ) : (
            <form onSubmit={handleSubmit(onSubmit)}>
              {getStepContent(step)}
            </form>
          )}
        </div>

        <div className="mt-6 flex justify-between">
          {step > 0 && (
            <Button
              color="blue"
              variant="outlined"
              onClick={prevStep}
              className="mr-2"
              disabled={loanStatus === "loading"}
            >
              Anterior
            </Button>
          )}
          {step < 1 ? (
            <Button
              color="blue"
              variant="filled"
              onClick={nextStep}
              className="ml-auto"
              disabled={loanStatus === "loading" || loanStatus === "error"}
            >
              Siguiente
            </Button>
          ) : (
            <Button
              onClick={handleSubmit(onSubmit)}
              type="submit"
              color="green"
              variant="filled"
              className="ml-auto"
              disabled={loanStatus === "loading"}
            >
              Enviar
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
