import React from "react";
import { Card, Button, Input } from "@material-tailwind/react";
import { LoansTable } from "./LoansTable";
const Loans = () => {
  return (
    <Card className="p-12 m-12 shadow-xl w-full shadow-blue-gray-900/">
      <LoansTable></LoansTable>
    </Card>
  );
};

export default Loans;
