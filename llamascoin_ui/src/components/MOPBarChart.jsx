import React from 'react';
import { BarChart } from '@mui/x-charts';

const MOPBarChart = ({ data }) => {
  return (
    <BarChart
      dataset={data}
      xAxis={[{ dataKey: 'label', label: 'Comportamiento de pagos (MOP)', scaleType: 'band' }]} // Configuramos el eje X como "band"
      yAxis={[{ label: 'Conteo' }]}
      series={[{ dataKey: 'value', label: 'Conteo de MOP' }]}
      width={500}
      height={400}
      layout="vertical"
      grid={{ vertical: false }}
    />
  );
};

export default MOPBarChart;
