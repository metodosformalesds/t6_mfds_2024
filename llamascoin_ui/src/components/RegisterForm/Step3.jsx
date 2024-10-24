import { React } from "react";
import { Input } from "@headlessui/react";
import { Typography } from "@material-tailwind/react";
import { formValidators } from "../../utils/formValidators";

export function Step3({ register, errors, defaultValues }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Información Fiscal</Typography>

      {/* Campo para RFC */}
      <div className="flex flex-col">
        <Input
          id="rfc"
          {...register("rfc", formValidators.rfc)}
          type="text"
          placeholder="RFC"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.rfc ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.rfc && <p className="text-red-500">{errors.rfc.message}</p>}</span>
      </div>

      {/* Campo para CIEC */}
      <div className="flex flex-col">
        <Input
          id="ciec"
          {...register("ciec", formValidators.ciec)}
          type="text"
          placeholder="CIEC"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.ciec ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.ciec && <p className="text-red-500">{errors.ciec.message}</p>}</span>
      </div>
    </div>
  );
}
