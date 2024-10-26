import React from "react";
import {
  Button,
  Dialog,
  DialogBody,
  DialogHeader,
  Typography,
} from "@material-tailwind/react";

export const ConfirmationModal = ({
  open,
  onClose,
  type,
  entity = "",
  onConfirm,
}) => {
  const title =
    type === "lender"
      ? "Confirmar solicitud al Prestamista"
      : "Confirmar solicitud al Prestatario";
  const message = `¿Seguro que desea solicitar el prestamo?`;
  return (
    <Dialog
      open={open}
      onClose={onClose}
      size="xs"
      className=" items-center justify-center"
    >
      <DialogBody className="flex flex-col justify-center items-center">
        <Typography variant="h3" color="blue-gray" className="text-center mb-4">
          {entity[0]}
        </Typography>
        <Typography variant="h5" color="blue-gray" className="text-center mb-4">
          {entity[1]}
        </Typography>

        <Typography color="blue-gray" className="text-center mb-4 ">
          {message}
        </Typography>
        <div className="flex gap-5">
          <Button onClick={onClose} variant="outlined" color="blue">
            Cancelar
          </Button>
          <Button onClick={onConfirm} color="blue">
            Confirmar
          </Button>
        </div>
      </DialogBody>
    </Dialog>
  );
};
