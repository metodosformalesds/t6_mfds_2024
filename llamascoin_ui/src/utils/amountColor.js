export const getAmountColor = (transactionType, role) => {
    if (role === "borrower") {
      if (transactionType === "payout") {
        return "text-green-500"; // Verde para "payout" si el rol es borrower
      } else if (transactionType === "payment") {
        return "text-red-500"; // Rojo para "payment" si el rol es borrower
      }
    } else if (role === "moneylender") {
      if (transactionType === "payout") {
        return "text-red-500"; // Rojo para "payout" si el rol es moneylender
      } else if (transactionType === "payment") {
        return "text-green-500"; // Verde para "payment" si el rol es moneylender
      }
    }
    return "text-gray-500"; // Color por defecto si no coincide con las condiciones
  };