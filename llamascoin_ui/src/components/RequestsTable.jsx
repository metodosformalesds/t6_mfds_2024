import { useEffect, useState } from "react";
import { XCircleIcon, CheckIcon } from "@heroicons/react/24/solid";
import { Button, Card, CardBody, CardHeader, Typography } from "@material-tailwind/react";
import { useAuth } from "../context/AuthContext";
import { useFetch } from "../hooks/useFetch";
import { ConfirmationModal } from "./ConfirmationModal";
import { apiHost } from "../utils/apiconfig";
import { ProfileCard } from "./ProfileCard";

const TABLE_HEAD = ["Prestatario", "Cantidad", "Plazos", "Acciones"];

export function RequestsTable() {
  const [tableRows, setTableRows] = useState([]);
  const { authData } = useAuth();
  const { status, data } = useFetch(apiHost + "request/");
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedEntity, setSelectedEntity] = useState("");
  const [entityType, setEntityType] = useState("");
  const [selectedRequestId, setSelectedRequestId] = useState("");

  

  useEffect(() => {

    if (status === "success" && data) {
      const rows = data.map((loan) => {
        const borrower = loan.borrower
          ? `${loan.borrower.first_name} ${loan.borrower.first_surname}`
          : "Desconocido";

        return {
          requestId: loan.id,
          borrower: borrower,
          amount: `$${parseFloat(loan.loan.amount).toFixed(2)}`,
          interest: `${loan.loan.interest_rate}%`,
          terms: `${loan.loan.term} meses`,
          status: loan.status || "Pendiente",
        };
      });

      setTableRows(rows);
    } else if (status === "error") {
      console.error("Error fetching data: ", error);
    }
  }, [status, data]);

  const handleStatusClick = (entity, type) => {
    
    setSelectedEntity(entity);
    setEntityType(type);
    setModalOpen(true);
  };

  const handleOpenModal = (type, requestId, borrower) => {
    setSelectedRequestId(requestId);
    setSelectedEntity(borrower);
    setEntityType(type);
    setModalOpen(true);
  };

  const handleAccept = () => {
    console.log("Aceptando solicitud para: ", selectedRequestId);
    setModalOpen(false);
  };


  const handleReject = () => {
    console.log("Rechazando solicitud para: ", selectedRequestId);
  
    setModalOpen(false); 
  };

  return (
    <Card className="h-full w-full shadow-none">
      <CardHeader floated={false} shadow={false} className="rounded-none">
        <div className="mb-4 flex flex-col justify-between gap-8 md:flex-row md:items-center">
          <div className="flex w-full shrink-0 gap-2 md:w-max">
            <Typography variant="h6" color="blue-gray">
              Lista de solicitudes
            </Typography>
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
            {tableRows.map(({requestId, borrower, amount, terms, status,  }, index) => {
              const isLast = index === tableRows.length - 1;
              const classes = isLast
                ? "p-4"
                : "p-4 border-b border-blue-gray-50";

              return (
                <tr key={index}>
                  <td className={classes}>
                    <Typography variant="small" color="blue-gray" className="font-bold">
                      {borrower}
                    </Typography>
                  </td>
                  <td className={classes}>
                    <Typography variant="small" color="blue-gray" className="font-normal">
                      {amount}
                    </Typography>
                  </td>
                  <td className={classes}>
                    <Typography variant="small" color="blue-gray" className="font-normal">
                      {terms}
                    </Typography>
                  </td>
                  <td className={classes}>
                    <div className="flex gap-2">
                      <Button
                        variant="text"
                        color="green"
                        size="md"
                        onClick={() => handleOpenModal('accept', requestId, borrower)} 
                      >
                        <CheckIcon className="h-5 w-5" />
                      </Button>
                      <Button
                        variant="text"
                        color="red"
                        size="md"
                        onClick={() => handleOpenModal('reject', requestId, borrower)}
                      >
                        <XCircleIcon className="h-5 w-5" />
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
      
        message={entityType === 'accept' ? "¿Seguro que desea aceptar el prestamo?" : "¿Seguro que desea cancelar el prestamo?"}
        entity={selectedEntity}
        onConfirm={entityType === 'accept' ? handleAccept : handleReject} 
      />
    </Card>
  );
}
