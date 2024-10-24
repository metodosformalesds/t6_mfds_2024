import {React, useState} from "react";
import { useForm } from "react-hook-form";
import { Input} from "@headlessui/react";
import { Typography, Button, Checkbox } from "@material-tailwind/react";
import { Link, useNavigate } from "react-router-dom";
import axios from 'axios'
import StatusComponent from "./StatusComponent";
import { formValidators } from "../utils/formValidators";
import { apiHost } from "../utils/apiconfig";
export function LoginForm({ onSubmit }) {
  const [status, setStatus] = useState("");
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();


 const submitHandler = async (data) => {
    const formData = new FormData();
    formData.append("username", data.email);
    formData.append("email", data.email);
    formData.append("password", data.password);
    setStatus("loading");

    try {
      const response = await axios.post(apiHost +'login/', formData, {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'multipart/form-data',
        }
      });

      console.log(response.data);
      setStatus("success");
      navigate('/home');


    } catch (error) {
      setStatus("error");
      console.error("Error al iniciar sesión:", error);
    }
  };


  return  (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md sm:px-10 p-5 shadow-lg rounded-lg">
        <form onSubmit={handleSubmit(submitHandler)} className="space-y-4">
          <Typography variant="h5" className="font-bold mb-4">
            Iniciar Sesión
          </Typography>

          <div className="flex flex-col">
            <Input
              id="email"
              {...register("email")}
              type="text"
              placeholder="Correo Electrónico"
              className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.email ? "border-red-500" : "border-gray-300"
              }`}
            />
            <span className="text-sm">
              {errors.email && <p className="text-red-500">{errors.email.message}</p>}
            </span>
          </div>

          <div className="flex flex-col">
            <Input
              id="password"
              {...register("password")}
              type="password"
              placeholder="Contraseña"
              className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.password ? "border-red-500" : "border-gray-300"
              }`}
            />
            <span className="text-sm">
              {errors.password && <p className="text-red-500">{errors.password.message}</p>}
            </span>
          </div>

          {/* Componente para mostrar el estado */}
          {(status === "loading" || status === "error" || status === "success") && (
            <StatusComponent status={status} />
          )}

          <Button type="submit" className="w-full bg-blue-500 text-white py-2 rounded-md">
            Iniciar Sesión
          </Button>

          <div className="flex items-center">
            <Checkbox
              color="blue"
              id="rememberMe"
              {...register("rememberMe")}
              label="Recuérdame"
              className="text-sm text-gray-600"
            />
          </div>

          <div className="text-center mt-4">
            <Typography variant="small" className="text-gray-600">
              ¿No tienes cuenta?{" "}
              <Link to="/register" className="text-blue-500 hover:underline">
                Regístrate
              </Link>
            </Typography>
          </div>
        </form>
      </div>
    </div>
  );
}
