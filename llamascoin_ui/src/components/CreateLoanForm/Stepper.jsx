import React from "react";

const Stepper = ({ currentStep }) => {
  const steps = [1, 2, 3]; // Definir el número de pasos
  //Diccionario para mantener agrupado el progreso
  const stepsKeys ={
    "0": 1,
    "1": 2,
    "2": 3,
  
  }
  return (
    <div className="flex items-center justify-center  w-full">
    <ol className="flex items-center  my-4">
      {steps.map((step, index) => (
        
        <li
          key={index}
          className={`flex w-full items-center ${
            index < steps.length - 1
              ? "after:content-[''] after:w-[75px] after:h-1 after:border-b after:border-4 after:inline-block " +
                (stepsKeys[currentStep] > step
                  ? "after:border-blue-100 dark:after:border-blue-800"
                  : "after:border-gray-100 dark:after:border-gray-300")
              : ""
          } ${stepsKeys[currentStep] >= step ? "text-blue-600 dark:text-blue-500" : ""}`}
        >
          <span
            className={`flex items-center justify-center w-8 h-8 ${
              stepsKeys[currentStep] >= step
                ? "bg-blue-100 dark:bg-blue-600 text-white "
                : "bg-gray-100 dark:bg-gray-300 text-gray-500 dark:text-gray-100"
            } rounded-full shrink-0`}
          >
            {stepsKeys[currentStep] > step ? (
              // Icono SVG de check si el paso está completado
              <svg
                className="w-3.5 h-3.5 lg:w-4 lg:h-4"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 16 12"
              >
                <path
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M1 5.917 5.724 10.5 15 1.5"
                />
              </svg>
            ) : (
              // Número del paso si aún no está completado
              <span className="text-sm font-medium">{step}</span>
            )}
          </span>
        </li>
      ))}
    </ol>
    </div>
  );
};

export default Stepper;
