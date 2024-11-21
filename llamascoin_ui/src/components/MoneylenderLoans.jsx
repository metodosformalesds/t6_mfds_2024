import { useEffect, useState } from "react";
import axios from "axios"; // Importa Axios
import { PencilIcon, XMarkIcon } from "@heroicons/react/24/outline";
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  Typography,
  Dialog,
  DialogBody,
} from "@material-tailwind/react";
import { useAuth } from "../context/AuthContext";
import { useFetch } from "../hooks/useFetch";
import { ConfirmationModal } from "./ConfirmationModal";
import { apiHost } from "../utils/apiconfig";
import { useNavigate } from "react-router-dom";
import { LoanSummary } from "./LoanSummary";
import { MultiStepLoanForm } from "./CreateLoanForm/MultiStepLoanForm";

const TABLE_HEAD = [
  "Monto",
  "Tasa de Interés (%)",
  "Tipo de Plazo",
  "Número de Pagos",
  "Fecha de Publicación",
  "Estado",
  "Acciones",
];

export const TERM_CHOICES = {
  1: "Semanal",
  2: "Quincenal",
  3: "Mensual",
};
const STATUS_CHOICES = {
  pending: "Pendiente",
  approved: "Aprobado",
  rejected: "Rechazado",
  completed: "Completado",
};

export function MoneylenderLoans() {
  const [loanRows, setLoanRows] = useState([]);
  const [selectedLoan, setSelectedLoan] = useState({});
  const { authData } = useAuth();
  const { status, data } = useFetch(apiHost + "loan/");
  const [modalOpen, setModalOpen] = useState(false);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (status === "success" && data) {
      setLoanRows(data);
    } else if (status === "error") {
      console.error("Error fetching data");
    }
  }, [status, data]);

  const handleSelectLoan = (loan, isEdit) => {
    setSelectedLoan(loan);
    if (isEdit){
      setEditModalOpen(true)
    }
    else{
      setModalOpen(true);
    }
    console.log(selectedLoan)
  };

  // Eliminar un préstamo
  const handleDelete = async () => {
    try {
      await axios.delete(`${apiHost}loan/${selectedLoan.id}/`, {
        headers: {
          Authorization: `Bearer ${authData.accessToken}`,
        },
      });
      console.log("Préstamo eliminado:", selectedLoan.borrower);
      setModalOpen(false);
      navigate(0);
    } catch (error) {
      console.error("Error deleting loan:", error);
    }
  };

  return (
    <Card className="h-full w-full shadow-none">
      <CardHeader floated={false} shadow={false} className="rounded-none">
        <div className="mb-4 flex flex-col justify-between gap-8 md:flex-row md:items-center">
          <Typography variant="h3" color="blue-gray">
            Mis préstamos
          </Typography>
        </div>
      </CardHeader>
      <CardBody className="px-0 overflow-y-auto h-[36em]">
        {loanRows.length === 0 ? (
          <div className="text-center">
            <Typography color="gray">No hay más registros</Typography>
          </div>
        ) : (
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
                if (loan.status === "En préstamo") statusColor = "amber";
                else if (loan.status === "Rechazado") statusColor = "red";
                else if (loan.status === "Disponible") statusColor = "green";

                return (
                  <tr key={loan.id}>
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
                        {TERM_CHOICES[loan.term] || "N/A"}
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
                          disabled={
                            loan.status === "Pagado" ||
                            loan.status === "Rechazado"
                          }
                        >
                          {loan.status || "Solicitar"}
                        </Button>
                      </div>
                    </td>
                    <td className={classes}>
                      <div className="flex gap-2">
                        {loan.status === "Disponible" && (
                          <>
                            <Button
                              variant="text"
                              color="blue"
                              size="sm"
                              onClick={() => handleSelectLoan(loan, true)}
                            >
                              <PencilIcon className="h-5 w-5" />
                            </Button>
                            <Button
                              variant="text"
                              color="red"
                              size="sm"
                              onClick={() => handleSelectLoan(loan, false)}
                            >
                              <XMarkIcon className="h-5 w-5" />
                            </Button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </CardBody>
      <Dialog open={editModalOpen} handler={()=>setEditModalOpen(false)}>
       <MultiStepLoanForm loanId={selectedLoan?.id} />

      </Dialog>
      <Dialog
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        size="xs"
        className="items-center justify-center"
      >
        <DialogBody className="flex flex-col justify-center items-center">
          <LoanSummary loanData={selectedLoan} serviceFeeLlamas={0.01}></LoanSummary>

          <Typography color="blue-gray" className="text-center my-4 ">
            ¿Seguro que desea eliminar el préstamo?
          
          </Typography>
          <div className="flex gap-5">
            <Button
              onClick={() => setModalOpen(false)}
              variant="outlined"
              color="blue"
            >
              Cancelar
            </Button>
            <Button 
            
            onClick={() => {
              handleDelete();
       
            }}
            color="blue">Confirmar</Button>
          </div>
        </DialogBody>
      </Dialog>
    </Card>
  );
}
