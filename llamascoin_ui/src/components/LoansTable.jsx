import { useEffect, useState } from "react";
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
const TABLE_HEAD = [
  "Prestamista",
  "Cantidad",
  "Interés",
  "Plazos",
  "Número de Pagos",
  "Fecha de Publicación",
  "Estado",
];

export function LoansTable() {
  const [tableRows, setTableRows] = useState([]);
  const { authData } = useAuth();
  const { status, data, error } = useFetch(apiHost + "loan/");
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedEntity, setSelectedEntity] = useState("");
  const [entityType, setEntityType] = useState("");

  useEffect(() => {
    if (status === "success" && data) {
      const rows = data.map((loan) => {
        const lender = loan.moneylender
          ? `${loan.moneylender.first_name} ${loan.moneylender.first_surname}`
          : "Desconocido";
        const borrower = loan.borrower
          ? `${loan.borrower.first_name} ${loan.borrower.first_surname}`
          : "Desconocido";

        return {
          lender: lender,
          borrower: borrower,
          amount: `$${parseFloat(loan.amount).toFixed(2)}`,
          interest: `${loan.interest_rate}%`,
          terms: `${loan.term} meses`,
          paymentCount: loan.number_of_payments,
          publishDate: loan.publication_date,
          status: loan.request_status || "Solicitar",
        };
      });

      setTableRows(rows);
    } else if (status === "error") {
      console.error("Error fetching data: ", error);
    }
  }, [status, data, error]);

  const handleStatusClick = (entity, type) => {
    setSelectedEntity(entity);
    setEntityType(type);
    setModalOpen(true);
  };

  const handleConfirm = () => {
    console.log(`Llamada confirmada para: ${selectedEntity}`);
    setModalOpen(false);
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
            {tableRows.map(
              (
                {
                  lender,
                  borrower,
                  amount,
                  interest,
                  terms,
                  paymentCount,
                  publishDate,
                  status,
                },
                index
              ) => {
                const isLast = index === tableRows.length - 1;
                const classes = isLast
                  ? "p-4"
                  : "p-4 border-b border-blue-gray-50";

                let statusColor = "blue";

                if (status === "pending") statusColor = "amber";
                else if (status === "rejected") statusColor = "red";

                return (
                  <tr key={index}>
                    <td className={classes}>
                      <div className="flex items-center gap-3">
                        <Typography
                          variant="small"
                          color="blue-gray"
                          className="font-bold"
                        >
                          {lender}
                        </Typography>
                      </div>
                    </td>
                    <td className={classes}>
                      <Typography
                        variant="small"
                        color="blue-gray"
                        className="font-normal"
                      >
                        {amount}
                      </Typography>
                    </td>
                    <td className={classes}>
                      <Typography
                        variant="small"
                        color="blue-gray"
                        className="font-normal"
                      >
                        {interest}
                      </Typography>
                    </td>
                    <td className={classes}>
                      <Typography
                        variant="small"
                        color="blue-gray"
                        className="font-normal"
                      >
                        {terms}
                      </Typography>
                    </td>
                    <td className={classes}>
                      <Typography
                        variant="small"
                        color="blue-gray"
                        className="font-normal"
                      >
                        {paymentCount}
                      </Typography>
                    </td>
                    <td className={classes}>
                      <Typography
                        variant="small"
                        color="blue-gray"
                        className="font-normal"
                      >
                        {publishDate}
                      </Typography>
                    </td>
                    <td className={classes}>
                      <div className="flex gap-2">
                        <Button
                          variant="filled"
                          color={statusColor}
                          size="md"
                          disabled={status == "pending"}
                          onClick={() => {
                            if (status !== "rejected") {
                              handleStatusClick([lender, amount], "lender");
                            }
                          }}
                        >
                          {status}
                        </Button>
                      </div>
                    </td>
                  </tr>
                );
              }
            )}
          </tbody>
        </table>
      </CardBody>
      <ConfirmationModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        type={entityType}
        entity={selectedEntity}
        onConfirm={handleConfirm}
      />
    </Card>
  );
}
