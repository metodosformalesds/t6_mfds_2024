import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
import { Box, Typography } from '@mui/material';
import { ArrowUpIcon } from '@heroicons/react/24/solid';
import ReactSpeedometer from 'react-d3-speedometer'


export default function ScoreCharts({ value, referenceValue }) {

  const scoreData = [
    { tier: 1, range: [465, 524], buenos: 0.20, malos: 12.67, intermedios: 2.00, morosidad: 98 },
    { tier: 2, range: [525, 538], buenos: 0.38, malos: 11.37, intermedios: 3.18, morosidad: 4.80 },
    { tier: 3, range: [539, 549], buenos: 0.57, malos: 11.40, intermedios: 4.11, morosidad: 5.10 },
    { tier: 4, range: [550, 559], buenos: 0.78, malos: 10.23, intermedios: 4.24, morosidad: 4.80 },
    { tier: 5, range: [560, 571], buenos: 1.13, malos: 10.36, intermedios: 4.93, morosidad: 5.10 },
    { tier: 6, range: [572, 584], buenos: 1.57, malos: 9.62, intermedios: 5.08, morosidad: 5.10 },
    { tier: 7, range: [585, 599], buenos: 2.30, malos: 8.74, intermedios: 5.21, morosidad: 5.10 },
    { tier: 8, range: [600, 614], buenos: 3.34, malos: 7.27, intermedios: 4.30, morosidad: 4.90 },
    { tier: 9, range: [615, 639], buenos: 4.70, malos: 4.92, intermedios: 6.69, morosidad: 5.10 },
    { tier: 10, range: [640, 654], buenos: 5.08, malos: 2.73, intermedios: 8.79, morosidad: 4.90 },
    { tier: 11, range: [655, 658], buenos: 2.25, malos: 0.89, intermedios: 2.75, morosidad: 1.80 },
    { tier: 12, range: [659, 667], buenos: 6.88, malos: 2.32, intermedios: 25.50, morosidad: 8.40 },
    { tier: 13, range: [668, 674], buenos: 7.07, malos: 1.74, intermedios: 4.09, morosidad: 4.60 },
    { tier: 14, range: [675, 682], buenos: 8.39, malos: 1.49, intermedios: 5.02, morosidad: 5.30 },
    { tier: 15, range: [683, 690], buenos: 7.77, malos: 1.13, intermedios: 4.23, morosidad: 4.80 },
    { tier: 16, range: [691, 698], buenos: 8.97, malos: 1.00, intermedios: 2.82, morosidad: 5.10 },
    { tier: 17, range: [699, 704], buenos: 9.36, malos: 0.72, intermedios: 1.57, morosidad: 4.90 },
    { tier: 18, range: [705, 712], buenos: 6.32, malos: 0.45, intermedios: 1.54, morosidad: 3.40 },
    { tier: 19, range: [713, 724], buenos: 12.84, malos: 0.61, intermedios: 1.98, morosidad: 6.60 },
    { tier: 20, range: [725, 760], buenos: 10.11, malos: 0.34, intermedios: 1.96, morosidad: 5.20 },
  ];

  const getTierData = (score) => {
    return scoreData.find(
      ({ range }) => score >= range[0] && score <= range[1]
    );
  };

  const tierData = getTierData(value);

  if (!tierData) {
    return (
      <div className="text-center text-red-500">
        <p>El score está fuera del rango de la tabla.</p>
      </div>
    );
  }

  return (
    <Box display="flex" flexDirection="column" alignItems="center" gap={3}>
      {/* Speedometer */}
      <ReactSpeedometer
        width={300}
        height={200}
        minValue={465}
        maxValue={760}
        segments={4}
        customSegmentLabels={[
          { text: "Muy Bajo", position: "INSIDE" },
          { text: "Bajo", position: "INSIDE" },
          { text: "Medio", position: "INSIDE" },
          { text: "Alto", position: "INSIDE" },
        ]}
        segmentColors={["#F97027", "#FEC300", "#8DC53F", "#56ba17"]}
        currentValueText={`${value} puntos`}
        value={parseInt(value, 10)}
      />


      <Box textAlign="center">
        <Typography variant="h6">
          El usuario está en un rango donde se encuentra el{' '}
          <span className="font-semibold">{tierData.buenos}%</span> de clientes buenos,
          el <span className="font-semibold">{tierData.malos}%</span> de clientes malos y un{' '}
          <span className="font-semibold">{tierData.intermedios}%</span> de clientes intermedios.
        </Typography>
        <Typography variant="body1" mt={2}>
          Con una tasa de morosidad del{' '}
          <span className="font-semibold">{tierData.morosidad}%</span>.
        </Typography>
      </Box>
    </Box>
  );
}