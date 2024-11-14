import React, { useEffect, useState } from "react";
import { LoanSummary } from "../LoanSummary";
export function Step2({ getValues }) {
  const [loanData, setLoanData] = useState({
    amount: 0,
    interest_rate: 0,
  });

  useEffect(() => {
    const values = getValues(); 

    if (values.amount && values.interest_rate) {
      setLoanData({
        amount: values.amount,
        interest_rate: values.interest_rate,
      });
    }
  }, [getValues]);

  return (
    <div className="space-y-4">
      <LoanSummary loanData={loanData} serviceFeeLlamas={0.01} />
   
    </div>
  );
}