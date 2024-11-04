import { React } from "react";
import { Input } from "@headlessui/react";
import { Typography } from "@material-tailwind/react";
import { formValidators } from "../../utils/formValidators";

export function Step3({ register, errors, defaultValues }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Validacion de identidad</Typography>

      {/* Contenedor para centrar la imagen */}
      <div className="flex justify-center items-center">
        {/* Añadir la imagen y asegurarse de que esté centrada */}
        <img src=".\src\assets\images\validation.png" alt="Validación de identidad" className="w-1/2 h-auto" />
      </div>

  
    </div>
  );
}
