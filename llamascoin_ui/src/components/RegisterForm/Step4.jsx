import { React } from "react";
import { Typography } from "@material-tailwind/react";
import { FaCheckCircle} from 'react-icons/fa';
export function Step4() {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">
        Identificación
      </Typography>

      {/* Icono de check */}
      <div className="flex items-center">
        <FaCheckCircle className="h-6 w-6 text-green-500 mr-2" />
        <span className="text-sm">Estamos revisando tu perfil.</span>
      </div>

      {/* Mensaje informativo */}
      <Typography variant="body1" className="text-gray-600 mt-2">
        Cuando todo esté listo te notificaremos. Podrás iniciar sesión y disfrutar de los beneficios de LlamasCoin.
      </Typography>
    </div>
  );
}
