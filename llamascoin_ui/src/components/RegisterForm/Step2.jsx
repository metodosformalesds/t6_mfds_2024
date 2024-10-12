import { React } from "react";
import { Input } from "@headlessui/react";
import { Typography } from "@material-tailwind/react";

export function Step2({ register, errors }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Dirección</Typography>

      {/* Campo para Dirección */}
      <div className="flex flex-col">
        <Input
          id="address"
          {...register("address", { required: "Este campo es requerido" })}
          type="text"
          placeholder="Dirección"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.address ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.address && <p className="text-red-500">{errors.address.message}</p>}</span>
      </div>

      {/* Campo para Municipio */}
      <div className="flex flex-col">
        <Input
          id="municipality"
          {...register("municipality", { required: "Este campo es requerido" })}
          type="text"
          placeholder="Municipio"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.municipality ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.municipality && <p className="text-red-500">{errors.municipality.message}</p>}</span>
      </div>

      {/* Campo para Código Postal */}
      <div className="flex flex-col">
        <Input
          id="postalCode"
          {...register("postalCode", { required: "Este campo es requerido" })}
          type="text"
          placeholder="Código Postal"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.postalCode ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.postalCode && <p className="text-red-500">{errors.postalCode.message}</p>}</span>
      </div>

      {/* Campo para Estado */}
      <div className="flex flex-col">
        <Input
          id="state"
          {...register("state", { required: "Este campo es requerido" })}
          type="text"
          placeholder="Estado"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.state ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.state && <p className="text-red-500">{errors.state.message}</p>}</span>
      </div>
    </div>
  );
}
