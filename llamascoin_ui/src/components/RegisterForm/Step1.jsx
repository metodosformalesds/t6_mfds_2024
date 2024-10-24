import { React, useState } from "react";
import { Input } from "@headlessui/react";
import { Typography } from "@material-tailwind/react";
import { formValidators } from "../../utils/formValidators";

export function Step1({ register, errors }) {
  const [inputType, setInputType] = useState('text');

  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Información Personal</Typography>

      {/* Campo para Nombre */}
      <div className="flex flex-col">
        <Input
          label="Primer Nombre"
          id="first_name"
          {...register("first_name", formValidators.first_name)}
          type="text"
          placeholder="Nombre"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.first_name ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.first_name && <p className="text-red-500">{errors.first_name.message}</p>}</span>
      </div>

      {/* Campo para Segundo Nombre (opcional) */}
      <div className="flex flex-col">
        <Input
          label="Segundo Nombre (opcional)"
          id="middle_name"
          {...register("middle_name", formValidators.middle_name)}
          type="text"
          placeholder="Segundo nombre (opcional)"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.middle_name ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.middle_name && <p className="text-red-500">{errors.middle_name.message}</p>}</span>
      </div>

      {/* Campo para Apellido Paterno */}
      <div className="flex flex-col">
        <Input
          label="Apellido Paterno"
          id="first_surname"
          {...register("first_surname", formValidators.first_surname)}
          type="text"
          placeholder="Apellido paterno"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.first_surname ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.first_surname && <p className="text-red-500">{errors.first_surname.message}</p>}</span>
      </div>

      {/* Campo para Apellido Materno (opcional) */}
      <div className="flex flex-col">
        <Input
          label="Apellido Materno (opcional)"
          id="second_surname"
          {...register("second_surname", formValidators.second_surname)}
          type="text"
          placeholder="Apellido materno"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.second_surname ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.second_surname && <p className="text-red-500">{errors.second_surname.message}</p>}</span>
      </div>

      {/* Campo para Fecha de Nacimiento */}
      <div className="flex flex-col">
        <Input
          label="Fecha de Nacimiento"
          id="birth_date"
          {...register("birth_date", formValidators.birth_date)}
          placeholder="Fecha de nacimiento"
          type={inputType} 
          onFocus={() => setInputType('date')} // Cambiar a tipo date al enfocar
          onBlur={() => setInputType('text')} // Cambiar a tipo text al desenfocar
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.birth_date ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.birth_date && <p className="text-red-500">{errors.birth_date.message}</p>}</span>
      </div>

      {/* Campo para Número de Teléfono */}
      <div className="flex flex-col">
        <Input
          label="Número de Teléfono"
          id="phone_number"
          {...register("phone_number", formValidators.phone_number)}
          type="text"
          placeholder="Número de teléfono"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.phone_number ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.phone_number && <p className="text-red-500">{errors.phone_number.message}</p>}</span>
      </div>
    </div>
  );
}
