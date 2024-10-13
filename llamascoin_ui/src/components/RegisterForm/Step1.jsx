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
          label="Nombre"
          id="firstName"
          {...register("firstName", formValidators.firstName)}
          type="text"
          placeholder="Nombre"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.firstName ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.firstName && <p className="text-red-500">{errors.firstName.message}</p>}</span>
      </div>

      {/* Campo para Apellido Paterno */}
      <div className="flex flex-col">
        <Input
          id="lastName"
          {...register("lastName",  formValidators.lastName)}
          type="text"
          placeholder="Apellido paterno"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.lastName ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.lastName && <p className="text-red-500">{errors.lastName.message}</p>}</span>
      </div>

      {/* Campo para Apellido Materno */}
      <div className="flex flex-col">
        <Input
          id="secondLastName"
          {...register("secondLastName",  formValidators.secondLastName)}
          type="text"
          placeholder="Apellido materno"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.secondLastName ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.secondLastName && <p className="text-red-500">{errors.secondLastName.message}</p>}</span>
      </div>

      {/* Campo para Fecha de Nacimiento */}
      <div className="flex flex-col">
        <Input
          id="birthdate"
          {...register("birthdate", formValidators.birthdate)}
          placeholder="Fecha de nacimiento"
          type={inputType} 
          onFocus={() => setInputType('date')} // Cambiar a tipo date al enfocar
          onBlur={() => setInputType('text')} // Cambiar a tipo text al desenfocar
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.birthdate ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.birthdate && <p className="text-red-500">{errors.birthdate.message}</p>}</span>
      </div>
    </div>
  );
}
