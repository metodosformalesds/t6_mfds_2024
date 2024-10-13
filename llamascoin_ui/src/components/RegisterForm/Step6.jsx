import { React } from "react";
import { Select, Option} from "@material-tailwind/react"; 
import { Typography } from "@material-tailwind/react";
import { formValidators } from "../../utils/formValidators";

export function Step6({ register, errors }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Tipo de Cuenta</Typography>

      {/* Campo para Tipo de Cuenta */}
      <div className="flex flex-col">
        <select
        
          id="accountType"
          
          {...register("accountType", formValidators.accountType)}
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.accountType ? 'border-red-500' : 'border-gray-300'
          }`}
        >
        
          <option value="prestamista">Prestamista</option>
          <option value="prestatario">Prestatario</option>
        </select>

        <span className="text-sm">{errors.accountType && <p className="text-red-500">{errors.accountType.message}</p>}</span>
      </div>
    </div>
  );
}
