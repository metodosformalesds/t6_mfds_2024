import { React } from "react";
import { Input } from "@headlessui/react";
import { Typography } from "@material-tailwind/react";
import { formValidators } from "../../utils/formValidators";

export function Step2({ register, errors, defaultValues }) {
  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">Dirección</Typography>

      {/* Campo para Dirección Completa */}
      <div className="flex flex-col">
        <Input
          label="Dirección Completa"
          id="full_address"
          {...register("full_address", formValidators.full_address)}
          type="text"
          placeholder="Dirección Completa"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.full_address ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.full_address && <p className="text-red-500">{errors.full_address.message}</p>}</span>
      </div>

      {/* Campo para Ciudad */}
      <div className="flex flex-col">
        <Input
          label="Ciudad"
          id="city"
          {...register("city", formValidators.city)}
          type="text"
          placeholder="Ciudad"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.city ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.city && <p className="text-red-500">{errors.city.message}</p>}</span>
      </div>

      {/* Campo para Vecindario */}
      <div className="flex flex-col">
        <Input
          label="Vecindario"
          id="neighborhood"
          {...register("neighborhood", formValidators.neighborhood)}
          type="text"
          placeholder="Vecindario"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.neighborhood ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.neighborhood && <p className="text-red-500">{errors.neighborhood.message}</p>}</span>
      </div>

      {/* Campo para Código Postal */}
      <div className="flex flex-col">
        <Input
          label="Código Postal"
          id="postal_code"
          {...register("postal_code", formValidators.postal_code)}
          type="text"
          placeholder="Código Postal"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.postal_code ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.postal_code && <p className="text-red-500">{errors.postal_code.message}</p>}</span>
      </div>

      {/* Campo para Estado */}
      <div className="flex flex-col">
        <Input
          label="Estado"
          id="state"
          {...register("state", formValidators.state)}
          type="text"
          placeholder="Estado"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.state ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.state && <p className="text-red-500">{errors.state.message}</p>}</span>
      </div>

      {/* Campo para País */}
      <div className="flex flex-col">
        <Input
          label="País"
          id="country"
          {...register("country", formValidators.country)}
          type="text"
          placeholder="País"
          className={`px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.country ? 'border-red-500' : 'border-gray-300'
          }`}
        />
        <span className="text-sm">{errors.country && <p className="text-red-500">{errors.country.message}</p>}</span>
      </div>
    </div>
  );
}
