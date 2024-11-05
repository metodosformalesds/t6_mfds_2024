import { React, useState } from "react";
import { Input } from "@headlessui/react";
import { Typography, Checkbox } from "@material-tailwind/react";
import { formValidators } from "../../utils/formValidators";

export function Step1({ register, errors }) {
  const [inputType, setInputType] = useState('text');

  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Información Personal</Typography>

      {/* Campo para Correo Electrónico */}
      <div className="flex flex-col">
        <Input
          label="Correo Electrónico"
          id="email"
          {...register("email", formValidators.email)}
          type="email"
          placeholder="Correo electrónico"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.email ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.email && <p className="text-red-500">{errors.email.message}</p>}</span>
      </div>

      {/* Campo para Contraseña */}
      <div className="flex flex-col">
        <Input
          label="Contraseña"
          id="password"
          {...register("password", formValidators.password)}
          type="password"
          placeholder="Contraseña"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.password ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.password && <p className="text-red-500">{errors.password.message}</p>}</span>
      </div>

      {/* Campo para CURP */}
      <div className="flex flex-col">
        <Input
          label="CURP"
          id="curp"
          {...register("curp", formValidators.curp)}
          type="text"
          placeholder="CURP"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.curp ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.curp && <p className="text-red-500">{errors.curp.message}</p>}</span>
      </div>

      {/* Checkbox para Términos y Condiciones */}

      <Checkbox
          id="terms"
          color="blue"
          {...register("terms", {
            required: "Debes aceptar los términos y condiciones",
          })}
          label={
            <span>
              Acepto los{" "}
              <a
                href="/terms"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 underline"
              >
                Términos y Condiciones
              </a>
            </span>
          }
          className="text-sm text-gray-600"
        />
        {errors.terms && (
          <p className="text-red-500 text-sm">{errors.terms.message}</p>
        )}

        <Checkbox
          id="privacyPolicy"
          color="blue"
          {...register("privacyPolicy", {
            required: "Debes aceptar la política de privacidad",
          })}
          label={
            <span>
              Acepto la{" "}
              <a
                href="/privacy_policy"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 underline"
              >
                Política de Privacidad
              </a>
            </span>
          }
          className="text-sm text-gray-600"
        />
        {errors.privacyPolicy && (
          <p className="text-red-500 text-sm">{errors.privacyPolicy.message}</p>
        )}
    
    </div>
  );
}
