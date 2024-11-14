import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { PieChart } from "@mui/x-charts/PieChart";

export default function LoanPercentage({ total_debt_paid, total_amount }) {
  const [radius] = React.useState(70);
  const [skipAnimation, setSkipAnimation] = React.useState(false);

  // Calcular el porcentaje pagado
  const percentagePaid = total_amount > 0 
  ? (parseFloat(total_debt_paid) / parseFloat(total_amount)) * 100 
  : 0; 
  // Definir los colores en función del porcentaje
  const getColor = (percentage) => {
    if (percentage >= 75) {
      return "#4caf50"; // Verde
    } else if (percentage >= 40) {
      return "#ffeb3b"; // Amarillo
    } else {
      return "#f44336"; // Rojo
    }
  };

  // Crear los datos para el gráfico con colores personalizados
  const data = [
    {
      label: "Porcentaje pagado",
      value: percentagePaid,
      color: getColor(percentagePaid),
    },
    {
      label: "Porcentaje restante",
      value: 100 - percentagePaid,
      color: "#9e9e9e", // Gris
    },
  ];

  return (
    <div className=" flex-col justify-center items-center">
      
      <PieChart
        className="flex items-center justify-center relative"
        height={200}
       
        series={[
          {
            data: data,
            innerRadius: radius,
            arcLabelMinAngle: 20,
            arcColor: (params) => params.data.color,
            cx: 200,
            cy: 100,
          },
        ]}
        slotProps={{
          legend: { hidden: true },
        }}
        skipAnimation={skipAnimation}
      />
    </div>
  );
}
