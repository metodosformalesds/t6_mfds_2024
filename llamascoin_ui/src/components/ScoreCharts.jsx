import * as React from 'react';
import Stack from '@mui/material/Stack';
import { PieChart } from '@mui/x-charts/PieChart';

// Datos iniciales
const data = [
  { label: 'Bajo', value: 100 },    
  { label: 'Normal', value: 100 },  
  { label: 'Alto', value: 100 },  
];

const colors = ['#ff0000', '#ffff00', '#008000']; // Rojo, Amarillo, Verde

const getScoreDistribution = (score = 25) => {
  const lowThreshold = 25;   // Umbral para rango bajo
  const highThreshold = 75;  // Umbral para rango alto

  // Inicializa la distribución
  const distribution = { low: 0, normal: 0, high: 0 };

  // Determina qué rangos deben ser pintados
  if (score <= lowThreshold) {
    distribution.low = 100;     // Pintar bajo
    distribution.normal = 0;    // No pintar normal
    distribution.high = 0;      // No pintar alto
  } else if (score <= highThreshold) {
    distribution.low = 100;     // Pintar bajo
    distribution.normal = 100;   // Pintar normal
    distribution.high = 0;      // No pintar alto
  } else {
    distribution.low = 100;     // Pintar bajo
    distribution.normal = 100;   // Pintar normal
    distribution.high = 100;     // Pintar alto
  }

  return distribution;
};

export default function ScoreCharts({ score }) {
  // Obtener la distribución según el score
  const scoreDistribution = getScoreDistribution(score);

  // Actualiza los datos según el score
  const updatedData = data.map((item, index) => ({
    ...item,
    value: scoreDistribution[item.label.toLowerCase()], // Asigna el valor basado en el score
  }));

  return (
    <Stack direction="row">
      <PieChart
        series={[
          {
            startAngle: -90,
            endAngle: 90,
            paddingAngle: 5,
            innerRadius: 60,
            outerRadius: 80,
            data: updatedData.map((item, index) => ({
              ...item,
              color: item.value > 0 ? colors[index] : 'transparent', // Asignar color o transparente
            })),
          },
        ]}
        margin={{ right: 5 }}
        width={200}
        height={200}
        slotProps={{
          legend: { hidden: true },
        }}
      />
    </Stack>
  );
}
