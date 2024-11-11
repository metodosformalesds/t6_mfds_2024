import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
import { Box, Typography } from '@mui/material';
import { ArrowUpIcon } from '@heroicons/react/24/solid';

const data = [
  { label: 'Group A', value: 33, color: "#F97027" }, // 0-33
  { label: 'Group B', value: 33, color: "#FEC300" }, // 34-66
  { label: 'Group C', value: 34, color: "#8DC53F" }, // 67-100
];
let segment = 1

export default function ScoreCharts() {
  const [value, setValue] = React.useState(50); // Valor actual que se puede modificar

  // Función para obtener el color y etiqueta según el valor
  const getColorAndLabel = () => {
    if (value <= 33) {
      segment = 1
      return { color: "#F97027", label: 'Group A' };
    }

    else if (value <= 66) {
      segment = 2
      return { color: "#FEC300", label: 'Group B' }}

    segment = 3
    return { color: "#8DC53F", label: 'Group C' };
  };

  // Obtener el ángulo de rotación en función del valor
  const getRotationAngle = () => {
    return (segment * 60) + 270; // Escala el valor de 0 a 100 a un rango de 0 a 180 grados
  };

  const { color, label } = getColorAndLabel();

  return (
    <Box display="flex" flexDirection="column" alignItems="center">
      <PieChart
        series={[
          {
            startAngle: -90,
            endAngle: 90,
            data,
          },
        ]}
        slotProps={{
          legend: { hidden: true },
        }}
        height={300}
      />
      <Box display="flex " alignItems="center" mt={2}>
       
        <Typography variant="h6" style={{ color, marginLeft: 8 }}>
          {label} ({value}%)
        </Typography>
      </Box>
      <ArrowUpIcon
          className='absolute '
          style={{
            width: '200px',
            color,
            fontSize: 30,
            transform: `rotate(${getRotationAngle()}deg)`, // Rota según el valor
          }}
        />
    </Box>
  );
}
