import React from "react";
import {
  Button,
  Dialog,
  DialogBody,
  DialogHeader,
  Typography,
} from "@material-tailwind/react";
import { ProfileCard } from "./ProfileCard";

export const ConfirmationModal = ({
  open,
  onClose,
  title,
  message,
  entity,

  onConfirm,
}) => {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      size="xs"
      className=" items-center justify-center"
    >
      {title && (
        <DialogHeader>
          <>{title}</>
        </DialogHeader>
      )}

      <DialogBody className="flex flex-col justify-center items-center">
        <ProfileCard entity={entity} />

        <Typography color="blue-gray" className="text-center my-4 ">
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
