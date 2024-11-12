import { useEffect, useState } from "react";
import { XCircleIcon, CheckIcon } from "@heroicons/react/24/solid";
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Dialog,
  DialogHeader,
  DialogBody,
  Typography,
  IconButton,
} from "@material-tailwind/react";
import { useAuth } from "../context/AuthContext";
import { useFetch } from "../hooks/useFetch";
import { ConfirmationModal } from "./ConfirmationModal";
import { apiHost } from "../utils/apiconfig";
import CreditHistory from "./CreditHistory";
import { PayPalCheckout } from "./PayPalCheckOut";
import axios from "axios";
import { useNavigate } from "react-router-dom";
const TABLE_HEAD = ["Prestatario", "Cantidad", "Plazos", "Acciones"];

export function RequestsTable() {
  const [requestRows, setRequestRows] = useState([]);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const { authData } = useAuth();
  const { status, data } = useFetch(apiHost + "request/");
  const [modalOpen, setModalOpen] = useState(false);
  const [creditHistoryOpen, setCreditHistoryOpen] = useState(false);
  const [paypalDialogOpen, setPaypalDialogOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (status === "success" && data) {
      setRequestRows(data);
    } else if (status === "error") {
      console.error("Error fetching data: ", status);
    }
  }, [status, data]);

  useEffect(() => {
    if (
      selectedRequest?.actionType == "accept" ||
      selectedRequest?.actionType == "reject"
    ) {
      setModalOpen(true);
    } else if (selectedRequest?.actionType == "creditHistory") {
      setCreditHistoryOpen(true);
    }
  }, [selectedRequest]);

  const handleSelectRequest = (request, type) => {
    setSelectedRequest({ ...request, actionType: type });
    console.log(selectedRequest);
  };

  const handleAccept = async () => {
    try {
      if (selectedRequest) {
        setModalOpen(false);
        setPaypalDialogOpen(true);
      }
    } catch (error) {
      console.error("Error accepting request: ", error);
    }
  };

  const handleReject = async () => {
    console.log("Rechazando solicitud para: ", selectedRequest.borrower);
    try {
      await axios.patch(
        `${apiHost}request/${selectedRequest.id}/`,
        {
          status: "rejected",
        },
        {
          headers: {
            Authorization: `Bearer ${authData.accessToken}`,
          },
        }
      );
      console.log("Solicitud rechazada para: ", selectedRequest.borrower);
      navigate(0);
      setModalOpen(false);
    } catch (error) {
      console.error("Error rejecting request: ", error);
    }
  };

  const handlePaypalSuccess = async (selectedRequest) => {
    try {
      await axios.patch(
        `${apiHost}request/${selectedRequest.id}/`,
        {
          status: "completed",
        },
        {
          headers: {
            Authorization: `Bearer ${authData.accessToken}`,
          },
        }
      );
      console.log("Solicitud completada para: ", selectedRequest.borrower);
      navigate(0);
      setPaypalDialogOpen(false);
    } catch (error) {
      console.error("Error completing request: ", error);
    }
  };

  return (
    <Card className=" w-full shadow-none">
      <CardHeader floated={false} shadow={false} className="rounded-none">
        <div className="mb-4 flex flex-col justify-between gap-8 md:flex-row md:items-center">
          <div className="flex w-full shrink-0 gap-2 md:w-max">
            <Typography variant="h6" color="blue-gray">
              Lista de solicitudes
            </Typography>
          </div>
        </div>
      </CardHeader>
      <CardBody className="px-0 py-0 max-h-[200px] overflow-y-auto">
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
          <tbody className="px-0 max-h-[200px] overflow-y-auto" >
            
            {requestRows.map((request, index) => {
              const isLast = index === requestRows.length - 1;
              const classes = isLast
                ? "p-4"
                : "p-4 border-b border-blue-gray-50";

              return (
                <tr key={index}>
                  <td className={classes}>
                    <Button
                      variant="text"
                      color="blue"
                      className="font-bold cursor-pointer"
                      onClick={() =>
                        handleSelectRequest(request, "creditHistory")
                      }
                    >
                      {request.borrower
                        ? `${request.borrower.first_name} ${request.borrower.first_surname}`
                        : "Desconocido"}
                    </Button>
                  </td>
                  <td className={classes}>
                    <Typography
                      variant="small"
                      color="blue-gray"
                      className="font-normal"
                    >
                      {request.loan.amount}
                    </Typography>
                  </td>
                  <td className={classes}>
                    <Typography
                      variant="small"
                      color="blue-gray"
                      className="font-normal"
                    >
                      {request.loan.term}
                    </Typography>
                  </td>
                  <td className={classes}>
                    <div className="flex gap-2">
                      {request.status === "pending" ? (
                        <>
                          <Button
                            variant="text"
                            color="green"
                            size="md"
                            onClick={() =>
                              handleSelectRequest(request, "accept")
                            }
                          >
                            <CheckIcon className="h-5 w-5" />
                          </Button>
                          <Button
                            variant="text"
                            color="red"
                            size="md"
                            onClick={() =>
                              handleSelectRequest(request, "reject")
                            }
                          >
                            <XCircleIcon className="h-5 w-5" />
                          </Button>
                        </>
                      ) : (
                        <Typography
                          variant="small"
                          color="gray"
                          className="font-normal"
                        >
                          {request.status === "approved"
                            ? "Aprobado"
                            : "Rechazado"}
                        </Typography>
                      )}
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
        message={
          selectedRequest?.actionType === "accept"
            ? "¿Seguro que desea aceptar el préstamo?"
            : "¿Seguro que desea cancelar el préstamo?"
        }
        entity={selectedRequest?.borrower}
        onConfirm={
          selectedRequest?.actionType === "accept" ? handleAccept : handleReject
        }
      />
      <Dialog size="xl" handler={setCreditHistoryOpen} open={creditHistoryOpen}>
       
        <CreditHistory borrowerId={selectedRequest?.borrower.id} />
      </Dialog>
      <Dialog size="sm" handler={setPaypalDialogOpen} open={paypalDialogOpen}>
        
        <div className="m-5">
        <PayPalCheckout
          loan={selectedRequest?.loan}
          person={selectedRequest?.borrower}
          onSuccess={() => {
            handlePaypalSuccess;
          }}
          onError={() => {
            setPaypalDialogOpen(false);
          }}
        />
        </div>
      </Dialog>
    </Card>
  );
}
