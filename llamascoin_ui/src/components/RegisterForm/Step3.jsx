import { React } from "react";
import { Input } from "@headlessui/react";
import { Typography } from "@material-tailwind/react";

export function Step3({ register, errors }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Información Fiscal</Typography>

      {/* Campo para RFC */}
      <div className="flex flex-col">
        <Input
          id="rfc"
          {...register("rfc", { required: "Este campo es requerido" })}
          type="text"
          placeholder="RFC"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.rfc ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.rfc && <p className="text-red-500">{errors.rfc.message}</p>}</span>
      </div>

      {/* Campo para Número */}
      <div className="flex flex-col">
        <Input
          id="number"
          {...register("number", { required: "Este campo es requerido" })}
          type="text"
          placeholder="Número"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.number ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.number && <p className="text-red-500">{errors.number.message}</p>}</span>
      </div>
    </div>
  );
}
