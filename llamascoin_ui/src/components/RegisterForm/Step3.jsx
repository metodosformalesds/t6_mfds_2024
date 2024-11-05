import { React } from "react";
import { Avatar } from "@material-tailwind/react"; // Asegúrate de que este import sea correcto según tu instalación
import { Typography } from "@material-tailwind/react";
import validationImage from "../../assets/images/validation.png"
export function Step3() {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Validación biométrica</Typography>

      {/* Componente Avatar */}
      <div className="flex flex-col items-center">
        <img 
          src={validationImage}
          alt="Validación de identidad"
        
        />

      </div>
    </div>
  );
}
