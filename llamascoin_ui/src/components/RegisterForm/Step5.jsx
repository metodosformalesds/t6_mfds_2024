import { React } from "react";
import { Typography } from "@material-tailwind/react";
import { formValidators } from "../../utils/formValidators";

export function Step5({ register, errors, defaultValues }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Tipo de Cuenta</Typography>

      {/* Campo para Tipo de Cuenta */}
      <div className="flex flex-col">
        <select
          id="account_type"
          {...register("account_type", formValidators.accountType)} 
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.account_type ? 'border-red-500' : 'border-gray-300'
          }`}
        >
          <option value="" disabled>Selecciona un tipo de cuenta</option>
          <option value="moneylender">Prestamista</option>
          <option value="borrower">Prestatario</option>
        </select>

        <span className="text-sm">{errors.account_type && <p className="text-red-500">{errors.account_type.message}</p>}</span>
      </div>
    </div>
  );
}
