import { React } from "react";
import { Input } from "@headlessui/react";
import { Typography } from "@material-tailwind/react";

export function Step7({ register, errors }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Credenciales</Typography>

      {/* Campo para Email */}
      <div className="flex flex-col">
        <Input
          id="email"
          {...register("email", { required: "Este campo es requerido" })}
          type="email"
          placeholder="Email"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.email ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.email && <p className="text-red-500">{errors.email.message}</p>}</span>
      </div>

      {/* Campo para Contraseña */}
      <div className="flex flex-col">
        <Input
          id="password"
          {...register("password", { required: "Este campo es requerido" })}
          type="password"
          placeholder="Contraseña"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.password ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.password && <p className="text-red-500">{errors.password.message}</p>}</span>
      </div>
    </div>
  );
}
