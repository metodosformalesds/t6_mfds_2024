import { React, useState } from "react";
import {
  Card,
  Button,
  Input,
  Typography,
  Dialog,
  DialogHeader,
  DialogBody,
  DialogFooter,
} from "@material-tailwind/react";
import CardDashboard from "./CardDashboard";
import { RequestsTable } from "./RequestsTable";
import { CurrencyDollarIcon } from "@heroicons/react/24/solid";
  const [open, setOpen] = useState(false);

  const handleOpen = () => setOpen(!open);

  return (
    <Card className="p-12 m-12 shadow-xl w-full shadow-blue-gray-900/ flex-col gap-3">
      <div className="flex justify-between">
        <Typography variant="h3" color="blue-gray">
          Inicio
        </Typography>
        <Button onClick={handleOpen} variant="filled" color="blue">
          Nuevo Prestamo
        </Button>
      </div>
      <div className="grid gap-5 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        <CardDashboard
          title="Dinero Prestado"
          icon={CurrencyDollarIcon}
          iconColor="text-green-500"
          value="$200"
        />
        <CardDashboard
          title="Dinero Prestado"
          icon={CurrencyDollarIcon}
          iconColor="text-green-500"
          value="$200"
        />
        <CardDashboard
          title="Dinero Prestado"
          icon={CurrencyDollarIcon}
          iconColor="text-green-500"
          value="$200"
        />
        <CardDashboard
          title="Dinero Prestado"
          icon={CurrencyDollarIcon}
          iconColor="text-green-500"
          value="$200"
        />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mt-5">
        <div className="flex flex-col">
          <Card className="flex-grow shadow-lg p-4">
            <RequestsTable />
          </Card>
          <Card className="flex-grow shadow-lg p-4 mt-4">
            <Typography variant="h5">Componente 2</Typography>
          </Card>
        </div>

        <div className="flex-grow"></div>
      </div>
      <div />

      <Dialog open={open} handler={handleOpen}>
      </Dialog>
    </Card>
  );
};

export default MoneylenderDashboard;
