import React, { useState, useEffect } from "react";
import { Card, Typography, Dialog } from "@material-tailwind/react";
import CardDashboard from "./CardDashboard";
import { ProfileCard } from "./ProfileCard";
import { MultiStepLoanForm } from "./CreateLoanForm/MultiStepLoanForm";
import {
  CurrencyDollarIcon,
  ClipboardDocumentIcon,
  LockClosedIcon,
  CalendarIcon,
} from "@heroicons/react/24/solid";
import { useAuth } from "../context/AuthContext";
import axios from "axios";
import { apiHost } from "../utils/apiconfig";
import MOPBarChart from "./MOPBarChart";
import { formatMOPData } from "../utils/formatMOPData";
import ScorePieCharts from "./ScoreCharts";

const CreditHistory = ({ borrowerId }) => {
  const { authData } = useAuth();
  const userId = borrowerId ? borrowerId : authData?.userId;
  const [creditHistory, setCreditHistory] = useState(null);
  const [open, setOpen] = useState(false);
  const [entity, setEntity] = useState(null);

  useEffect(() => {
    const fetchCreditHistory = async () => {
      try {
        const endpoint = `${apiHost}borrower/${userId}/`;

        const response = await axios.get(endpoint, {
          headers: {
            Authorization: `Bearer ${authData.accessToken}`,
            accept: "application/json",
          },
        });

        const data = response.data;
        const entityName = `${data.first_name} ${data.middle_name} ${data.first_surname} ${data.second_surname}`;

        setEntity(data);
        setCreditHistory(data.credit_history[0]);
      } catch (error) {
        console.error("Error fetching credit history:", error);
      }
    };

    if (userId) {
      fetchCreditHistory();
    }
  }, [userId]);

  const handleOpen = () => setOpen(!open);

  const content = (
    <>
      <div className="flex justify-between">
        <Typography variant="h3" color="blue-gray">
          Historial crediticio
        </Typography>
      </div>
  
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mt-5">
        <div className="grid grid-cols-1 gap-5">
          <Card className="shadow-lg p-4 mt-4 col-span-1">
            {creditHistory ? (
              <ProfileCard entity={entity} />
            ) : (
              <p>Cargando historial crediticio...</p>
            )}
  
            <div className="grid grid-cols-3 gap-4 mt-4">
              <div className="flex flex-col items-center">
                <Typography color="gray">Pago actual</Typography>
                <Typography variant="h6" className="font-bold cursor-pointer">
                  {creditHistory?.current_pay_status || "N/A"}
                </Typography>
              </div>
              <div className="flex flex-col items-center">
                <Typography color="gray">Historial</Typography>
                <Typography variant="h6" className="font-bold cursor-pointer">
                  {creditHistory?.pay_history || "N/A"}
                </Typography>
              </div>
              <div className="flex flex-col items-center">
                <Typography color="gray">Lugar de trabajo</Typography>
                <Typography variant="h6" className="font-bold cursor-pointer">
                  {creditHistory?.place_of_work || "N/A"}
                </Typography>
              </div>
            </div>
          </Card>
  
          <Card className="shadow-lg p-4 mt-4">
            <ScorePieCharts code_score={creditHistory?.code_score} />
          </Card>
        </div>
  
        <div className="grid grid-cols-1 gap-5">
          {creditHistory ? (
            <MOPBarChart data={formatMOPData(creditHistory) || {}} />
          ) : (
            <p>Cargando datos de MOP...</p>
          )}
  
          <Card className="shadow-lg p-4 mt-4">
            <div className="grid grid-cols-3 gap-4 mt-4">
              <div className="flex flex-col items-center">
                <Typography color="gray">Cuentas abiertas</Typography>
                <Typography variant="h6" className="font-bold">
                  {creditHistory?.accounts_open || "N/A"}
                </Typography>
              </div>
              <div className="flex flex-col items-center">
                <Typography color="gray">Cuentas cerradas</Typography>
                <Typography variant="h6" className="font-bold">
                  {creditHistory?.accounts_closed || "N/A"}
                </Typography>
              </div>
              <div className="flex flex-col items-center">
                <Typography color="gray">Cuentas fijas</Typography>
                <Typography variant="h6" className="font-bold">
                  {creditHistory?.account_fixed_payment || "N/A"}
                </Typography>
              </div>
            </div>
          </Card>
        </div>
      </div>
  
      <Dialog open={open} handler={handleOpen}>
        <MultiStepLoanForm />
      </Dialog>
  
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-5">
        <CardDashboard
          title="Saldo pendiente"
          icon={CurrencyDollarIcon}
          iconColor="text-green-500"
          value={`$${creditHistory?.actual_balance || "N/A"}`}
        />
        <CardDashboard
          title="Máximo crédito"
          icon={ClipboardDocumentIcon}
          iconColor="text-blue-500"
          value={`$${creditHistory?.max_credit || "N/A"}`}
        />
        <CardDashboard
          title="Límite crédito"
          icon={LockClosedIcon}
          iconColor="text-yellow-500"
          value={`$${creditHistory?.lim_credit || "N/A"}`}
        />
        <CardDashboard
          title="Fecha de apertura"
          icon={CalendarIcon}
          iconColor="text-pink-500"
          value={creditHistory?.date_account_open || "N/A"}
        />
      </div>
    </>
  );
  
  return borrowerId ? (
    <div className="p-12 mx-12 pt-0">
      {content}
    </div>
  ) : (
    <Card className="p-12 m-12 shadow-xl w-full shadow-blue-gray-900/">
      {content}
    </Card>
  );

};

export default CreditHistory;
