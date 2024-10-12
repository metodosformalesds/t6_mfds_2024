import { React } from "react";
import { Input } from "@headlessui/react";
import { Typography } from "@material-tailwind/react";

export function Step5({ register, errors }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Datos Financieros</Typography>

      {/* Campo para CLABE */}
      <div className="flex flex-col">
        <Input
          id="clabe"
          {...register("clabe", { required: "Este campo es requerido" })}
          type="text"
          placeholder="CLABE"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.clabe ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.clabe && <p className="text-red-500">{errors.clabe.message}</p>}</span>
      </div>

      {/* Campo para Tarjeta de Crédito */}
      <div className="flex flex-col">
        <Input
          id="creditCard"
          {...register("creditCard", { required: "Este campo es requerido" })}
          type="text"
          placeholder="Número de tarjeta de crédito"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.creditCard ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.creditCard && <p className="text-red-500">{errors.creditCard.message}</p>}</span>
      </div>
    </div>
  );
}
