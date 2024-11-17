import { React, useState, useEffect } from "react";
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
import {
  CurrencyDollarIcon,
  BanknotesIcon,
  UserGroupIcon,
  UsersIcon,
  ArrowUpCircleIcon,
} from "@heroicons/react/24/solid";
import { MultiStepLoanForm } from "./CreateLoanForm/MultiStepLoanForm";
import { AbstractTable } from "./AbstractTable";
import { apiHost } from "../utils/apiconfig";
import { useAuth } from "../context/AuthContext";
import { useFetch } from "../hooks/useFetch";

const sampleData = {
  stats: {
    active_loans: [
      {
        id: 1,
        borrower: {
          id: 101,
          first_name: "John Doe",
          first_surname: "john.doe@example.com",
          rfc: "https://via.placeholder.com/100",
        },
        loan_amount: 1000,
        total_debt_paid: "500.00",
        amount_to_pay: "500.00",
        start_date: "2024-10-16",
        payments: [
          {
            number_of_pay: 1,
            date_to_pay: "2024-11-16",
            paid: true,
            paid_on_time: true,
          },
          {
            number_of_pay: 2,
            date_to_pay: "2024-12-16",
            paid: false,
            paid_on_time: false,
          },
          {
            number_of_pay: 2,
            date_to_pay: "2024-12-19",
            paid: false,
            paid_on_time: false,
          },
          {
            number_of_pay: 2,
            date_to_pay: "2024-12-22",
            paid: false,
            paid_on_time: false,
          },
          {
            number_of_pay: 2,
            date_to_pay: "2024-12-26",
            paid: false,
            paid_on_time: false,
          },
          {
            number_of_pay: 2,
            date_to_pay: "2024-12-29",
            paid: false,
            paid_on_time: false,
          },
 
        ],
      },
      {
        id: 2,
        borrower: {
          id: 102,
          name: "Jane Smith",
          email: "jane.smith@example.com",
          profile_picture: "https://via.placeholder.com/100",
        },
        loan_amount: 2000,
        total_debt_paid: "1500.00",
        amount_to_pay: "500.00",
        start_date: "2024-09-10",
        payments: [
          {
            number_of_pay: 1,
            date_to_pay: "2024-10-10",
            paid: true,
            paid_on_time: true,
          },
          {
            number_of_pay: 2,
            date_to_pay: "2024-11-10",
            paid: true,
            paid_on_time: false,
          },
          {
            number_of_pay: 3,
            date_to_pay: "2024-12-10",
            paid: false,
            paid_on_time: false,
          },
        ],
      },
    ],
  },
};



const MoneylenderDashboard = () => {
  const [open, setOpen] = useState(false);
  const [dashboardStats, setDashboardStats] = useState();
  const { authData } = useAuth();
  const { status, data } = useFetch(apiHost + `moneylender/`);

  useEffect(() => {
    if (status === "success" && data) {
      if (data.stats) {
        setDashboardStats(data.stats);
      }
    } else if (status === "error") {
      console.error("Error fetching data: ", error);
    }
  }, [status, data]);

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
          title="Ganancias totales"
          icon={BanknotesIcon}
          iconColor="text-green-500"
          value={`$${dashboardStats ? dashboardStats.total_earnings : 0}`}
        />

        <CardDashboard
          title="Dinero Prestado"
          icon={UserGroupIcon}
          iconColor="text-blue-500"
          value={`$${dashboardStats ? dashboardStats.total_loans : 0}`}
        />

        <CardDashboard
          title="Prestamos activos"
          icon={UsersIcon}
          iconColor="text-yellow-500"
          value={dashboardStats ? dashboardStats.total_active_loans : 0}
        />

        <CardDashboard
          title="Dinero en deuda"
          icon={ArrowUpCircleIcon}
          iconColor="text-red-500"
          value={`$${
            dashboardStats ? dashboardStats.total_pending_balance : 0
          }`}
        />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mt-5">
        <div className="flex flex-col">
          <Card className="flex-grow shadow-lg p-4">
            <RequestsTable />
          </Card>
          <Card className="flex-grow shadow-lg p-4 mt-4">
            <AbstractTable
              tableHeaders={{
                "PayPal ID": "paypal_transaction_id",
                Monto: "amount_paid",
                "Fecha de Pago": "payment_date",
                Persona: "person",
              }}
              apiUrl={apiHost + "transaction"}
              title={"Historial de pagos"}
            ></AbstractTable>
          </Card>
        </div>

        <div className="flex-grow"></div>
      </div>
      <div />

      <Dialog open={open} handler={handleOpen}>
        <MultiStepLoanForm />
      </Dialog>
    </Card>
  );
};

export default MoneylenderDashboard;


