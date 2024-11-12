import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
import { Box, Typography } from '@mui/material';
import { ArrowUpIcon } from '@heroicons/react/24/solid';
import ReactSpeedometer from 'react-d3-speedometer'

export default function ScoreCharts({value, referenceValue}) {
 

  return (
   
      <ReactSpeedometer
      width={300}
        height={200}
        minValue={0}
        maxValue={referenceValue}
        segments={4}
        customSegmentLabels={[
          {
          text:"Muy Bajo",
          position:"INSIDE"
        },
        {
          text:"Bajo",
          position:"INSIDE"
        },
        {
          text:"Medio",
          position:"INSIDE"
        },
        {
          text:"Alto",
          position:"INSIDE"
        }
      ]}
      
        segmentColors={["#F97027", "#FEC300", "#8DC53F", "#56ba17"]}
        currentValueText={`${value} puntos`}
        value={parseInt(value, 10)}
      
      />
  
  );
}
