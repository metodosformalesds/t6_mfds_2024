export const formatMOPData = (apiResponse) => {
    return [
      { label: "MOP 1", value: apiResponse.num_mop1 },
      { label: "MOP 2", value: apiResponse.num_mop2 },
      { label: "MOP 3", value: apiResponse.num_mop3 },
      { label: "MOP 4", value: apiResponse.num_mop4 },
      { label: "MOP 5", value: apiResponse.num_mop5 },
      { label: "MOP 6", value: apiResponse.num_mop6 },
      { label: "MOP 7", value: apiResponse.num_mop7 },
    ];
  };
  