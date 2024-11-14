import React, { useEffect, useState } from "react";
import { Typography } from "@material-tailwind/react";
import ReactSpeedometer from "react-d3-speedometer";

export function LoanSummary({ loanData, serviceFeeLlamas }) {
  const [loan, setLoan] = useState({
    amount: 0,
    amountWithInterest: 0,
    interest: 0,
    paypalFee: 0,
    serviceFee: 0,
    fixedFee: 0,
    totalAmountToPay: 0,
  });

  useEffect(() => {
    const { amount, interest_rate } = loanData;

    if (amount && interest_rate) {
      const amountParsed = parseFloat(amount); 
      const interestRateParsed = parseFloat(interest_rate);


      const interest = amountParsed * (interestRateParsed / 100); 
      const amountWithInterest = amountParsed * (1 + interestRateParsed / 100); 
      const paypalFee = amountParsed * 0.04; 
      const serviceFee = amountParsed * serviceFeeLlamas; 
      const fixedFee = 0.25; 
      const totalAmountToPay = amountParsed + paypalFee + serviceFee + fixedFee; 

      setLoan({
        amount: amountParsed,
        amountWithInterest,
        interest,
        paypalFee,
        serviceFee,
        fixedFee,
        totalAmountToPay,
      });
    }
  }, [loanData]);

  return (
    <div className="space-y-4">
      <Typography variant="h5" className="font-bold mb-4">
        Resumen del Préstamo
      </Typography>

      <div className="space-y-2">
        <div className="flex justify-between">
          <Typography variant="body1" className="font-semibold">
            Monto a Prestar:
          </Typography>
          <Typography variant="body1">${loan.amount.toFixed(2)}</Typography>
        </div>
        <div className="flex justify-between">
          <Typography variant="body1" className="font-semibold">
            Monto con Intereses:
          </Typography>
          <Typography variant="body1">${loan.amountWithInterest.toFixed(2)}</Typography>
        </div>
        <div className="flex justify-between">
          <Typography variant="body1" className="font-semibold">
            Ganancia (Intereses):
          </Typography>
          <Typography variant="body1">${loan.interest.toFixed(2)}</Typography>
        </div>
        <div className="flex justify-between">
          <Typography variant="body1" className="font-semibold">
            Tarifa de Paypal:
          </Typography>
          <Typography variant="body1">${loan.paypalFee.toFixed(2)}</Typography>
        </div>
        <div className="flex justify-between">
          <Typography variant="body1" className="font-semibold">
            Tarifa de Servicio:
          </Typography>
          <Typography variant="body1">${loan.serviceFee.toFixed(2)}</Typography>
        </div>
        <div className="flex justify-between">
          <Typography variant="body1" className="font-semibold">
            Tarifa Fija:
          </Typography>
          <Typography variant="body1">${loan.fixedFee.toFixed(2)}</Typography>
        </div>
        <div className="flex justify-between">
          <Typography variant="body1" className="font-semibold">
            Monto Total a Pagar:
          </Typography>
          <Typography variant="body1">${loan.totalAmountToPay.toFixed(2)}</Typography>
        </div>
      </div>

      <div>
      <Typography variant="h5" className="font-bold mb-4">
        Dificultad del prestamo
      </Typography>
      <ReactSpeedometer
 
        height={200}
        minValue={100}
        maxValue={10000}
        segments={4}
        customSegmentLabels={[
          { text: "Muy Bajo", position: "INSIDE" },
          { text: "Bajo", position: "INSIDE" },
          { text: "Medio", position: "INSIDE" },
          { text: "Alto", position: "INSIDE" },
        ]}
        segmentColors={["#F97027", "#FEC300", "#8DC53F", "#56ba17"]}
        currentValueText={`${loan.amount.toFixed(2)} puntos`}
        value={loan.amount}
      />
      </div>

   
    </div>
  );
}
