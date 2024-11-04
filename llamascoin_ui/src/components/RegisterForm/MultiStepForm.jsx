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
import { apiHost } from "../../utils/apiconfig";
import { useAuth } from "../../context/AuthContext";

export function MultiStepForm() {
  const [status, setStatus] = useState("");
  const [step, setStep] = useState(0);
  const navigate = useNavigate();
  const { login, authData } = useAuth(); 

  const { register, handleSubmit, formState: { errors }, getValues } = useForm({
    defaultValues: {
      email: "",
      password: "",  
      rfc: "",
      account_type: "",
    },
  });

  
  const onSubmit = async () => {
    const formData = getValues();
    const { email, password, account_type, curp } = formData;

    try {
      setStatus("loading");
      const response = await axios.post(apiHost + "register/", { email, password, account_type, curp }, {
        headers: { "Content-Type": "application/json" }
      });

      if (response.status === 201) {
        setStatus("success");
        await login(response.data);
        navigate("/home");
      } else {
        setStatus("error");
      }
    } catch (error) {
      setStatus("error");
    }
  };

  const steps = [
    <Step1 register={register} errors={errors} />,
    <Step2 register={register} errors={errors} />,
    <Step3 register={register} errors={errors} />,
    <Step4 register={register} errors={errors} />
  ];

  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <div className="flex flex-col justify-between sm:mx-auto sm:w-full min-h-[500px] sm:max-w-md sm:px-10 p-5 shadow-lg rounded-lg">
        <div>
          <Typography variant="h3" className="font-bold">Crear cuenta</Typography>
          <Stepper currentStep={step} />
          {status ? <StatusComponent status={status} /> : <form>{steps[step]}</form>}
        </div>

        <div className="mt-6 flex justify-between">
          {step > 0 && (
            <Button color="blue" variant="outlined" onClick={() => setStep(step - 1)} className="mr-2" disabled={status === "loading"}>
              Anterior
            </Button>
          )}
          {status === "error" ? (
            <Button color="blue" variant="filled" onClick={() => setStatus("")} className="ml-auto">
              Reintentar
            </Button>
          ) : (
            step < steps.length - 1 ? (
              <Button color="blue" variant="filled" onClick={() => setStep(step + 1)} className="ml-auto" disabled={status === "loading"}>
                Siguiente
              </Button>
            ) : (
              <Button onClick={handleSubmit(onSubmit)} color="green" variant="filled" className="ml-auto" disabled={status === "loading"}>
                Enviar
              </Button>
            )
          )}
        </div>
      </div>
    </div>
  );
}
