import { React } from "react";
import { Input } from "@headlessui/react";
import { Typography } from "@material-tailwind/react";
import { formValidators } from "../../utils/formValidators";

export function Step4({ register, errors }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Identificación</Typography>

      {/* Campo para Imagen de Identificación */}
      <div className="flex flex-col">
        <Input
          id="identificationImage"
          {...register("identificationImage", formValidators.identificationImage)}
          type="file"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.identificationImage ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.identificationImage && <p className="text-red-500">{errors.identificationImage.message}</p>}</span>
      </div>
    </div>
  );
}
