import { useState } from "react";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import { apiHost } from "../utils/apiconfig";
import { useAuth } from "../context/AuthContext";



export function PayPalCheckout({ loan, person, onSuccess, onError }) {
  const [orderID, setOrderID] = useState(null);
  const { authData } = useAuth();
  const createOrder = async () => {
    console.log("Creando orden con", loan)
    try {
      const response = await fetch(`${apiHost}paypal/create-checkout/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${authData.accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          loan_id: loan.id, 
          amount: loan.amount, 
        }),
      });

      if (!response.ok) {
        throw new Error("Error creating PayPal order");
      }

      const data = await response.json();
      setOrderID(data.orderID); 
      return data.orderID;
    } catch (error) {
      onError();
      console.error("Error creating order:", error);
    }
  };

  const onApprove = async (data) => {
    try {
      const response = await fetch(`${apiHost}paypal/capture-checkout/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${authData.accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          orderID: data.orderID,
          loan_id: loan.id, 
          person_id: person.id,
        }),
      });

      if (!response.ok) {
        throw new Error("Error capturing PayPal order");
      }

      onSuccess();
    } catch (error) {
      onError();
      console.error("Error capturing order:", error);
    }
  };

  return (
    <PayPalScriptProvider options={{ "client-id": "AS64qtQYEXejSTE5SpX9JXETJjgrCXOpqiDyMfWTXNZKXenaNIigapqnRMtBWuZNcdHSOLnCeugOvadu" }}>
      <PayPalButtons
        createOrder={() => createOrder()} 
        onApprove={(data) => {
          console.log("Approval data:", data);
          return onApprove(data);
        }} 
        onError={(error) => {
          console.error("PayPal Checkout onError", error);
          onError();
        }}
      />
    </PayPalScriptProvider>
  );
}
