import { useEffect, useState } from "react";
import axios from "axios"; // Importa Axios
import { PencilIcon } from "@heroicons/react/24/solid";
import {
  ArrowDownTrayIcon,
  MagnifyingGlassIcon,
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
      }
      
      if (data.active_loan) {
          setActiveLoan(data.active_loan); // Si hay un préstamo activo, configurar activeLoan
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

  return (
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
            <Button color="blue" className="flex items-center gap-3" size="sm">
              <ArrowDownTrayIcon strokeWidth={2} className="h-4 w-4" /> Buscar
            </Button>
            <Button
              color="blue"
              variant="outlined"
              className="flex items-center gap-3"
              size="sm"
            >
              <ArrowDownTrayIcon strokeWidth={2} className="h-4 w-4" /> Filtros
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
                      {loan.amount} MXN
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
                        disabled={loan.request_status === "pending"}
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
      </CardBody>
      <ConfirmationModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        type={entityType}
        message={"¿Seguro que desea solicitar el prestamo?"}
        entity={selectedLoan.moneylender}
        onConfirm={handleConfirm}
      />
    </Card>
  );
}
