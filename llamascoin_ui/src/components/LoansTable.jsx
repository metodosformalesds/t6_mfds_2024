import { useEffect, useState } from "react";
import axios from "axios"; // Importa Axios
import {
  PencilIcon,
  BanknotesIcon,
  CalendarIcon,
  CreditCardIcon,
} from "@heroicons/react/24/solid";
import {
  ArrowDownTrayIcon,
  MagnifyingGlassIcon,
  CurrencyDollarIcon,
} from "@heroicons/react/24/outline";
import {
  Card,
  CardHeader,
  Typography,
  Button,
  CardBody,
  Input,
} from "@material-tailwind/react";
import { useAuth } from "../context/AuthContext";
import { useFetch } from "../hooks/useFetch";
import { ConfirmationModal } from "./ConfirmationModal";
import { apiHost } from "../utils/apiconfig";
import { useNavigate } from "react-router-dom";
import CardDashboard from "./CardDashboard";
import { ProfileCard } from "./ProfileCard";
import { AbstractTable } from "./AbstractTable";
import Calendar from "./calendar";
import LoanPercentage from "./LoanPercentage";
import { PayPalCheckout } from "./PayPalCheckOut";

const TABLE_HEAD = [
  "Prestamista",
  "Cantidad",
  "Interés",
  "Plazos",
  "Número de Pagos",
  "Fecha de Publicación",
  "Estado",
];
const TERM_CHOICES = {
  1: "Semanal",
  2: "Quincenal",
  3: "Mensual",
};
const STATUS_CHOICES = {
  pending: "Pending", // Pendiente
  approved: "Approved", // Aprobado
  rejected: "Rejected", // Rechazado
  completed: "Completed", // Completado
};

export function LoansTable() {
  const [loanRows, setLoanRows] = useState([]);
  const [activeLoan, setActiveLoan] = useState();
  const [lastPendingPayment, setLastPendingPayment] = useState();
  const { authData } = useAuth();
  const { status, data, error } = useFetch(apiHost + "loan/");
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedLoan, setSelectedLoan] = useState("");
  const [entityType, setEntityType] = useState("");
  const [loanId, setLoanId] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    if (status === "success" && data) {
      if (data.loans) {
        setLoanRows(data.loans); // Si hay préstamos, configurar loanRows
        console.log(data)
      }

      if (data.active_loan) {
        console.log(data.active_loan);
        setActiveLoan(data.active_loan); // Si hay un préstamo activo, configurar activeLoan
        const pendingPayment = data.active_loan.payments.find(
          (payment) => payment.paid === false
        );
        setLastPendingPayment(pendingPayment);
      }
    } else if (status === "error") {
      console.error("Error fetching data: ", error);
    }
  }, [status, data, error]);

  const handleStatusClick = (loan) => {
    setSelectedLoan(loan);
    setModalOpen(true);
  };

  const handleConfirm = async () => {
    try {
      const response = await axios.post(
        apiHost + "request/",
        {
          moneylender_id: selectedLoan.moneylender.id,
          loan_id: selectedLoan.id,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authData.accessToken}`,
          },
        }
      );

      console.log("Llamada confirmada para: ", selectedLoan);
      console.log("Respuesta de la API: ", response.data);
      navigate(0);
      setModalOpen(false);
    } catch (error) {
      console.error("Error al confirmar la solicitud: ", error);
    }
  };

  const handlePaypalSuccess = async () => {
      navigate(0);
  };


  return (
    <>
      {!activeLoan ? (
        <Card className="h-full w-full shadow-none">
          <CardHeader floated={false} shadow={false} className="rounded-none">
            <div className="mb-4 flex flex-col justify-between gap-8 md:flex-row md:items-center">
              <div>
                <Typography variant="h3" color="blue-gray">
                  Prestamos
                </Typography>
              </div>
              <div className="flex w-full shrink-0 gap-2 md:w-max">
                <div className="w-full md:w-72">
                  <Input
                    label="Buscar"
                    icon={<MagnifyingGlassIcon className="h-5 w-5" />}
                  />
                </div>
                <Button
                  color="blue"
                  className="flex items-center gap-3"
                  size="sm"
                >
                  <ArrowDownTrayIcon strokeWidth={2} className="h-4 w-4" />{" "}
                  Buscar
                </Button>
                <Button
                  color="blue"
                  variant="outlined"
                  className="flex items-center gap-3"
                  size="sm"
                >
                  <ArrowDownTrayIcon strokeWidth={2} className="h-4 w-4" />{" "}
                  Filtros
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardBody className="px-0">
          <table className="w-full min-w-max table-auto text-left">
          <thead>
            <tr>
              {TABLE_HEAD.map((head) => (
                <th
                  key={head}
                  className="border-y border-blue-gray-100 bg-blue-gray-50/50 p-4"
                >
                  <Typography
                    variant="small"
                    color="blue-gray"
                    className="font-normal leading-none opacity-70"
                  >
                    {head}
                  </Typography>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loanRows.map((loan, index) => {
              const isLast = index === loanRows.length - 1;
              const classes = isLast
                ? "p-4"
                : "p-4 border-b border-blue-gray-50";

              let statusColor = "blue";

              if (loan.request_status === "pending") statusColor = "amber";
              else if (loan.request_status === "rejected") statusColor = "red";
              else if (loan.request_status === "completed") statusColor = "green";
              return (
                <tr key={index}>
                  <td className={classes}>
                    <div className="flex items-center gap-3">
                      <Typography
                        variant="small"
                        color="blue-gray"
                        className="font-bold"
                      >
                        {loan.moneylender.first_name +
                          " " +
                          loan.moneylender.first_surname}
                      </Typography>
                    </div>
                  </td>
                  <td className={classes}>
                    <Typography
                      variant="small"
                      color="blue-gray"
                      className="font-normal"
                    >
                      {loan.total_amount} MXN
                    </Typography>
                  </td>
                  <td className={classes}>
                    <Typography
                      variant="small"
                      color="blue-gray"
                      className="font-normal"
                    >
                      {loan.interest_rate}%
                    </Typography>
                  </td>
                  <td className={classes}>
                    <Typography
                      variant="small"
                      color="blue-gray"
                      className="font-normal"
                    >
                      {TERM_CHOICES[loan.term] || "Unknown Term"}
                    </Typography>
                  </td>
                  <td className={classes}>
                    <Typography
                      variant="small"
                      color="blue-gray"
                      className="font-normal"
                    >
                      {loan.number_of_payments}
                    </Typography>
                  </td>
                  <td className={classes}>
                    <Typography
                      variant="small"
                      color="blue-gray"
                      className="font-normal"
                    >
                      {loan.publication_date}
                    </Typography>
                  </td>
                  <td className={classes}>
                    <div className="flex gap-2">
                      <Button
                        variant="filled"
                        color={statusColor}
                        size="md"
                        disabled={loan.request_status === "pending" || loan.request_status==="completed" || loan.request_status==="approved"}
                        onClick={() => {
                          if (loan.request_status !== "rejected") {
                            handleStatusClick(loan);
                          }
                        }}
                      >
                        {loan.request_status === ""
                          ? "Solicitar"
                          : loan.request_status === "rejected"
                          ? STATUS_CHOICES["rejected"]
                          : STATUS_CHOICES[loan.request_status]}
                      </Button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <ConfirmationModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        type={entityType}
        message={"¿Seguro que desea solicitar el prestamo?"}
        entity={selectedLoan.moneylender}
        onConfirm={handleConfirm}
      />
          </CardBody>
        </Card>
      ) : (
        <Card className="h-full w-full shadow-none gap-5">
          <div className="flex justify-between">
            <Typography variant="h3" color="blue-gray">
              Inicio
            </Typography>
          </div>
          <div className="grid gap-5 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
            <CardDashboard
              title="Monto Pagado"
              icon={BanknotesIcon}
              iconColor="text-green-500"
              value={`$${activeLoan.total_debt_paid}`}
            />
            <CardDashboard
              title="Interés del Préstamo"
              icon={CurrencyDollarIcon}
              iconColor="text-blue-500"
              value={`${activeLoan.loan.interest_rate}%`}
            />
            <CardDashboard
              title="Tipo de Pago"
              icon={CreditCardIcon}
              iconColor="text-purple-500"
              value={TERM_CHOICES[activeLoan.loan.term] || "No especificado"}
            />
            <CardDashboard
              title="Saldo Restante"
              icon={CalendarIcon}
              iconColor="text-red-500"
              value={`$${activeLoan.amount_to_pay}`}
            />
          </div>
          <div className="w-full grid grid-cols-3 gap-4 h-[470px]">
         
            <div className="col-span-1 row-span-4 flex flex-col  flex-grow">
              
              <Card className="row-span-2 shadow-lg p-6 justify-evenly t flex-grow">
                <Typography
                  variant="h5"
                  color="blue-gray"
                  className="font-normal leading-none opacity-70"
                >
                  Porcentaje completado
                </Typography>
                <LoanPercentage
                  total_amount={activeLoan.loan.total_amount}
                  total_debt_paid={activeLoan.total_debt_paid}
                ></LoanPercentage>
                {lastPendingPayment ? (
                    <>
                      <Typography className="text-center">
                        Proximo pago el {lastPendingPayment.date_to_pay}
                      </Typography>
                      <PayPalCheckout
                        onSuccess={handlePaypalSuccess}
                        loan={{
                          id: activeLoan.loan.id,
                          amount: activeLoan.loan.payment_per_term,
                        }}
                        person={activeLoan.moneylender}
                      />
                    </>
                  ) : (
                    <div className="flex flex-col justify-center items-center gap-5">
                      <Typography variant="h4" className="text-center  text-green-500">
                      Préstamo pagado
                    </Typography>
                    <Button color="blue">Finalizar prestamo</Button>
                    </div>
                  )}
                
              </Card>
            </div>
            {/* Segunda columna (con Calendar) */}
            <Card className="col-span-1 row-span-4 shadow-lg p-4 flex-grow max-h-full overflow-y-auto">
              <Calendar payments={activeLoan.payments}></Calendar>
            </Card>
            {/* Tercera columna */}
            <div className="col-span-1 row-span-4 flex flex-col gap-4 flex-grow">
              <Card className="row-span-2 shadow-lg p-4 flex-grow">
                <ProfileCard entity={activeLoan.moneylender} />
                <div className="grid grid-cols-3 gap-4 mt-4">
              <div className="flex flex-col items-center">
                <Typography color="gray">Dinero recibido</Typography>
                <Typography variant="h6" className="font-bold cursor-pointer">
                {activeLoan?.loan.total_amount || "N/A"} MXN
                </Typography>
              </div>
              <div className="flex flex-col items-center">
                <Typography color="gray">Dificultad</Typography>
                <Typography variant="h6" className="font-bold cursor-pointer">
                 
                  {activeLoan?.loan.difficulty || "N/A"}
                </Typography>
              </div>
              <div className="flex flex-col items-center">
                <Typography color="gray">Publicación</Typography>
                <Typography variant="h6" className="font-bold cursor-pointer">
                {activeLoan?.loan.publication_date || "N/A"}
                </Typography>
              </div>
            </div>
              </Card>
              <Card className="row-span-2 shadow-lg p-4 flex-grow">
                <AbstractTable
                  title="Historial de transacciones"
                  tableHeaders={{
                    "PayPal ID": "paypal_transaction_id",
                    Monto: "amount_paid",
                    "Fecha de Pago": "payment_date",
                  }}
                  apiUrl={`${apiHost}/transaction`}
                />
              </Card>
            </div>
          </div>
        </Card>
      )}
    </>
  );
}
