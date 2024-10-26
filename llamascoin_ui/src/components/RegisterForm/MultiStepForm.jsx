import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import Stepper from "./Stepper";
import { Step1 } from "./Step1";
import { Step2 } from "./Step2";
import { Step3 } from "./Step3";
import { Step4 } from "./Step4";
import { Step5 } from "./Step5";
import { Step6 } from "./Step6";
import { Button, Typography } from "@material-tailwind/react";
import { Link, useNavigate } from "react-router-dom";
import StatusComponent from "../StatusComponent";
import axios from "axios";
import { apiHost } from "../../utils/apiconfig";
import { useAuth } from "../../context/AuthContext";

export function MultiStepForm() {
  const [status, setStatus] = useState("");
  const navigate = useNavigate();
  const { login, authData } = useAuth(); 
  const {
    register,
    handleSubmit,
    formState: { errors },
    trigger,
    getValues,
  } = useForm({
    defaultValues: {
      // Step 1: Información Personal
      first_name: "Adrian", // Primer nombre
      middle_name: "", // Segundo nombre (opcional)
      first_surname: "Rivas", // Primer apellido
      second_surname: "Escarcega", // Segundo apellido (opcional)
      birth_date: "", // Fecha de nacimiento
      phone_number: "", // Número de teléfono

      // Step 2: Información de Dirección
      full_address: "", // Dirección completa
      city: "", // Ciudad
      neighborhood: "", // Vecindario, barrio o colonia
      postal_code: "", // Código postal
      state: "", // Estado
      country: "", // País

      // Step 3: Información Fiscal
      rfc: "RIEA0301088K9", // Registro Federal de Contribuyentes
      ciec: "", // Clave de Identificación Electrónica Confidencial

      // Step 4: Información de Identificación
      identification_image: "", // Imagen de identificación (puede ser archivo)

      // Step 5: Tipo de Cuenta
      account_type: "", // Tipo de cuenta (puede ser "prestamista" o "prestatario")

      // Step 6: Credenciales de Usuario
      email: "", // Correo electrónico
      password: "", // Contraseña    // Puntaje de calificación
    },
  });

  useEffect(() => {
    if (authData.accessToken) {
      navigate('/home'); 
    }
  }, [authData, navigate]);
  
  const [step, setStep] = useState(0);
 

  const onSubmit = async () => {
    // Obtener todos los valores del formulario
    const formData = getValues();
  
    const {
      email,
      password,
      account_type, // "borrower" o "moneylender"
      first_name,
      middle_name,
      first_surname,
      second_surname,
      birth_date,
      phone_number,
      rfc,
      ciec,
      full_address,
      city,
      neighborhood,
      postal_code,
      state,
      country,
    } = formData;
  
    // Construir el objeto para el registro
    const dataToSubmit = {
      username: email, // Mismo que el email
      email: email,
      password: password,
      account_type: account_type,
      [account_type]: { // "borrower" o "moneylender"
        first_name: first_name,
        middle_name: middle_name,
        first_surname: first_surname,
        second_surname: second_surname,
        birth_date: birth_date,
        phone_number: phone_number,
        rfc: rfc,
        ciec: ciec,
        full_address: full_address,
        city: city,
        neighborhood: neighborhood,
        postal_code: postal_code,
        state: state,
        country: country,
      },
    };
  
    try {
      setStatus("loading");
      const response = await axios.post(
        apiHost+ "register/",
        dataToSubmit,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
  
      // Manejar la respuesta de la API
      if (response.status === 201) {
        setStatus("success");
        console.log("Registro exitoso:", response.data);
        await login(response.data)
        navigate('/home');
      } else {
        setStatus("error");
        console.error("Error en el registro:", response.data);
      }
    } catch (error) {
      console.error("Error al registrar:", error);
      setStatus("error");
    }
  };
  const nextStep = async () => {
    const result = await trigger();
    if (result) {
   
    
    if (step === 3) {
      const fullName = `${getValues("first_name")} ${getValues(
        "middle_name"
      )} ${getValues("first_surname")} ${getValues("second_surname")}`;
      const rfc = getValues("rfc");
      const image = getValues("identification_image")[0];

      const formDataToSend = new FormData();
      formDataToSend.append("image", image);
      formDataToSend.append("full_name", fullName);
      formDataToSend.append("rfc", rfc);

      try {
        setStatus("loading");
        const response = await axios.post(
          apiHost+ "validate_ine/",
          formDataToSend,
          {
            headers: {
              accept: "application/json",
              "Content-Type": "multipart/form-data",
            },
          }
        );

        // Verifica si la respuesta es exitosa
        if (
          response.status === 200 &&
          response.data.refresh &&
          response.data.access
        ) {
          setAccessToken(response.data.access);
          setStatus("success");
          setStep((currentStep) => currentStep + 1);
          setStatus("");
        } else {
          setStatus("error");
          console.error(
            "Error: La respuesta no contiene los datos esperados",
            response.data
          );
        }
      } catch (error) {
        console.error("Error al validar:", error);
        setStatus("error");
      }
    } else {
      setStep((currentStep) => currentStep + 1);
    }
  }
  };
  const prevStep =() =>{
    setStatus("");
    setStep((currentStep) => currentStep - 1);
  }

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
      default:
        return "No hay paso definido";
    }
  }

  return (
    <div className="flex  min-h-full flex-1   flex-col justify-center px-6 py-12 lg:px-8">
      <div className="flex flex-col justify-between sm:mx-auto sm:w-full min-h-[500px] sm:max-w-md sm:px-10 p-5 shadow-lg rounded-lg ">
        <div>
          <Typography variant="h3" className="font-bold">
            Crear cuenta
          </Typography>
          <Stepper currentStep={step} />

          {status === "loading" ||
          status === "error" ||
          status === "success" ? (
            <StatusComponent status={status} />
          ) : (
            <form>{getStepContent(step)}</form>
          )}
        </div>

        <div className="mt-6 flex justify-between">
          {step > 0 && (
            <Button
              color="blue"
              variant="outlined"
              onClick={prevStep}
              className="mr-2"
              disabled={status === "loading"}
            >
              Anterior
            </Button>
          )}
          {status === "error" && step===3 ?  (
            <Button
              color="blue"
              variant="filled"
              onClick={()=>setStatus('')}
              className="ml-auto"
            >
              Reintentar
            </Button>
          ) : (
            step < 5 && (
              <Button
                color="blue"
                variant="filled"
                onClick={nextStep}
                className="ml-auto"
                disabled={status === "loading"}
              >
                Siguiente
              </Button>
            )
          )}
          {step === 5 && (
            <Button
              onClick={handleSubmit(onSubmit)}
              color="green"
              variant="filled"
              className="ml-auto"
              disabled={status === "loading"}
            >
              Enviar
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
