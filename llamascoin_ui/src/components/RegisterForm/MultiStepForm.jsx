import React, { useState } from "react";
import { useForm } from "react-hook-form";
import Stepper from "./Stepper";
import { Step1 } from "./Step1";
import {Step2} from "./Step2";
import {Step3} from "./Step3";
import {Step4} from "./Step4";
import {Step5} from "./Step5";
import {Step6} from "./Step6";
import {Step7} from "./Step7";
import { Button, Typography } from "@material-tailwind/react";

export function MultiStepForm() {

  const {
    register,
    handleSubmit,
    formState: { errors },
    trigger,
  } = useForm({
    defaultValues: {
      //Step 1
      firstName: "",
      lastName: "",
      secondLastName: "",
      birthdate: "",

      //Step 2
      address: "",
      municipality: "",
      postalCode: "",
      state: "",

      //Step 3
      rfc: "",
      number: "",

      //Step 4
      identificationImage: "",

      //Step 5
      clabe: "",
      creditCard: "",

      //Step 6
      accountType: "",

      //Step 7
      email: "",
      password: "",
    },
  });
  const [step, setStep] = useState(0);

  const onSubmit = (formData) => {
    //LLamada a la api Django para la creacion con fetch o axios
    window.alert("Datos del formulario: " + JSON.stringify(formData));
  };

  const nextStep = async () => {
    const result = await trigger();
    if (result) {
      setStep((currentStep) => currentStep + 1);
    }
  };
  const prevStep = () => setStep((currentStep) => currentStep - 1);

  function getStepContent(step) {
    switch (step) {
      case 0:
        return <Step1 register={register} errors={errors} />;
      case 1:
        return <Step2 register={register} errors={errors} />;
      case 2:
        return <Step3 register={register} errors={errors} />;
      case 3:
        return <Step4 register={register} errors={errors} />;
      case 4:
        return <Step5 register={register} errors={errors} />;
      case 5:
        return <Step6 register={register} errors={errors} />;
      case 6:
        return <Step7 register={register} errors={errors} />;
      default:
        return "No hay paso definido";
    }
  }
  

  return (
    <div className="flex  min-h-full flex-1   flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md sm:px-10 p-5 shadow-lg rounded-lg ">
        <Typography variant="h3" className="font-bold">
          Crear cuenta
        </Typography>
        <Stepper currentStep={step} />
        <form>
          {getStepContent(step)}

          <div className="mt-6 flex justify-between">
            {step > 0 && (
              <Button
                color="blue"
                variant="outlined"
                onClick={prevStep}
                className="mr-2"
              >
                Anterior
              </Button>
            )}
            {step < 6 && (
              <Button
                color="blue"
                variant="filled"
                onClick={nextStep}
                className="ml-auto"
              >
                Siguiente
              </Button>
            )}
            {step === 6 && (
              <Button
                onClick={handleSubmit(onSubmit)}
                color="green"
                variant="filled"
                className="ml-auto"
              >
                Enviar
              </Button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
