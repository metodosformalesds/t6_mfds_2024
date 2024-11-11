export const formatMOPData = (apiResponse) => {
  return [

    { label: "1 a 29 días", value: apiResponse.num_mop2 },
    { label: "30 a 59 días", value: apiResponse.num_mop3 },
    { label: "60 a 89 días", value: apiResponse.num_mop4 },
    { label: "90 a 119 días", value: apiResponse.num_mop5 },
    { label: "120 a 149 días", value: apiResponse.num_mop6 },
    { label: "150 días a 12 meses", value: apiResponse.num_mop7 },
    { label: "Fraude", value: apiResponse.num_mop99 },
  ];
};
