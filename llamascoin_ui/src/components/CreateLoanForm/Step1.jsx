import React, { useState, useEffect } from "react";
import { CheckIcon } from "@heroicons/react/24/solid";
import { PayPalScriptProvider, PayPalButtons } from '@paypal/react-paypal-js';
import StatusComponent from "../StatusComponent";
export function Step1({ loanStatus, setLoanStatus }) {


  return (
    <div className="space-y-4">
      {loanStatus === "success" && (
       
        <StatusComponent status="success" customMessage="¡Cuenta con suscripción!" />
      )}
       
      {loanStatus === "error" && (
        <div>
          <div className="relative bg-gray-900 shadow-2xl rounded-3xl p-8 ring-1 ring-gray-900/10 sm:p-10">
            <h3 className="text-indigo-400 text-base font-semibold leading-7">
              Plan Prestamista
            </h3>
            <p className="mt-4 flex items-baseline gap-x-2">
              <span className="text-white text-5xl font-bold tracking-tight">
                $50
              </span>
              <span className="text-gray-400 text-base">/mes</span>
            </p>
            <p className="text-gray-300 mt-6 text-base leading-7">
              Accede a los beneficios de prestar dinero.
            </p>
            <ul role="list" className="text-gray-300 mt-8 space-y-3 text-sm leading-6 sm:mt-10">
              <li className="flex gap-x-3">
                <CheckIcon aria-hidden="true" className="text-indigo-400 h-6 w-5 flex-none" />
                Publica hasta 5 prestamos
              </li>
              <li className="flex gap-x-3">
                <CheckIcon aria-hidden="true" className="text-indigo-400 h-6 w-5 flex-none" />
                Accede a informacion de los prestatarios
              </li>
              <li className="flex gap-x-3">
                <CheckIcon aria-hidden="true" className="text-indigo-400 h-6 w-5 flex-none" />
                Elige a quien prestar
              </li>
              <li className="flex gap-x-3">
                <CheckIcon aria-hidden="true" className="text-indigo-400 h-6 w-5 flex-none" />
                Notificaciones
              </li>
              <li className="flex gap-x-3">
                <CheckIcon aria-hidden="true" className="text-indigo-400 h-6 w-5 flex-none" />
                Dashboard con tus ganancias
              </li>
              <PayPalScriptProvider 
                options={{
                  "client-id": "AS64qtQYEXejSTE5SpX9JXETJjgrCXOpqiDyMfWTXNZKXenaNIigapqnRMtBWuZNcdHSOLnCeugOvadu", 
                  "vault": true, 
                  "intent": "subscription",
                }}
              >
                <PayPalButtons
                  createSubscription={(data, actions) => {
                    return actions.subscription.create({
                      plan_id: "P-47J93263U52095012M4PTLFQ", 
                    });
                  }}
                  onApprove={(data, actions) => {
                    console.log("Subscription successful:", data);
                    setLoanStatus("success");
                    
                    alert("¡Suscripción completada con éxito!");
                  }}
                  onError={(err) => {
                    console.error("Error en la suscripción:", err);
                    setLoanStatus("error");
                    alert("Hubo un problema al procesar la suscripción.");
                  }}
                  style={{
                    layout: 'vertical',
                  }}
                />
              </PayPalScriptProvider>
            </ul>
          </div>

       
        </div>
      )}
    </div>
  );
}

export default Step1;
