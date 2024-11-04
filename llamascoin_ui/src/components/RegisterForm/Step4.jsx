import { React } from "react";
import { Input } from "@headlessui/react";
import { Typography } from "@material-tailwind/react";
import { formValidators } from "../../utils/formValidators";

export function Step4({ register, errors, defaultValues }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Identificación</Typography>

      {/* Mensaje */}
      <Typography className="text-center text-gray-600">
        Estamos revisando tu perfil<br />
        Cuando todo esté listo te notificaremos<br />
        Podrás iniciar sesión y disfrutar de los beneficios de llamasCoin
      </Typography>
      
    </div>
  );
}
