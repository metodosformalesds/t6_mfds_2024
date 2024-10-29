import { React, useState } from "react";
import {Input, Select, Option} from "@material-tailwind/react";
import { Typography } from "@material-tailwind/react";
import { formValidators } from "../../utils/formValidators";

export function Step2({ register, errors }) {
  const [inputType, setInputType] = useState('text');

  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Información del Préstamo</Typography>

      {/* Campo para Monto */}
      <div className="flex flex-col">
        <Input

          label="Cantidad"
          id="amount"
          {...register("amount", { 
            required: "La cantidad es obligatoria", 
            min: { value: 1, message: "La cantidad debe ser mayor que 0" }, 
            max: { value: 999999, message: "El monto no puede exceder 999,999" },
          })}
          type="number"
          placeholder="Cantidad"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2   ${
            errors.amount ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.amount && <p className="text-red-500">{errors.amount.message}</p>}</span>
      </div>

      {/* Selector de Plazos */}
      <div className="flex flex-col">
        <select
        label="Plazos"
          id="term"
          {...register("term", { required: "El plazo es obligatorio" })}
          className={`border rounded-md focus:outline-none focus:ring-2   ${
            errors.term ? 'border-red-500' : 'border-gray-300'
          }`}
        >
       
          <option value="1">Semanal</option>
          <option value="2">Quincenal</option>
          <option value="3">Mensual</option>
        </select>
    

        <span className="text-sm">{errors.term && <p className="text-red-500">{errors.term.message}</p>}</span>
      </div>

      {/* Campo para Tasa de Interés */}
      <div className="flex flex-col">
        <Input
          label="Tasa de Interés (%)"
          id="interest_rate"
          {...register("interest_rate", { 
            required: "La tasa de interés es obligatoria", 
            min: { value: 0, message: "La tasa de interés debe ser al menos 0" },
            max: { value: 25, message: "La tasa de interés no puede ser más del 25%" },
          })}
          type="number"
          placeholder="Tasa de interés"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2   ${
            errors.interest_rate ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.interest_rate && <p className="text-red-500">{errors.interest_rate.message}</p>}</span>
      </div>

      {/* Campo para Número de Pagos */}
      <div className="flex flex-col">
        <Input
          label="Número de Pagos"
          id="number_of_payments"
          {...register("number_of_payments", { 
            required: "El número de pagos es obligatorio", 
            min: { value: 1, message: "Debe ser al menos 1" }, 
            max: { value: 99, message: "No puede exceder 99" },
          })}
          type="number"
          placeholder="Número de pagos"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2   ${
            errors.number_of_payments ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.number_of_payments && <p className="text-red-500">{errors.number_of_payments.message}</p>}</span>
      </div>
    </div>
  );
}
