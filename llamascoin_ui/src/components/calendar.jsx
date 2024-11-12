import React, { useState } from "react";
import dayjs from "dayjs";
import "dayjs/locale/es"; // Importar el idioma español
import { Typography } from "@material-tailwind/react";
// Establecer el idioma a español
dayjs.locale("es");

const Calendar = ({ payments }) => {
  const [currentDate, setCurrentDate] = useState(dayjs());
  const today = dayjs(); // Día actual

  // Función para mover al mes anterior
  const handlePreviousMonth = () => {
    setCurrentDate(currentDate.subtract(1, "month"));
  };

  // Función para mover al mes siguiente
  const handleNextMonth = () => {
    setCurrentDate(currentDate.add(1, "month"));
  };

  // Generar las fechas del calendario del mes actual
  const generateCalendar = () => {
    const startOfMonth = currentDate.startOf("month");
    const endOfMonth = currentDate.endOf("month");
    const startDate = startOfMonth.startOf("week");
    const endDate = endOfMonth.endOf("week");

    let days = [];
    let day = startDate;

    // Generamos todos los días del mes actual, incluso los días que no pertenecen a este mes
    while (day.isBefore(endDate, "day")) {
      days.push(day);
      day = day.add(1, "day");
    }
    return days;
  };

  const days = generateCalendar();

  // Función para verificar si un día tiene un pago programado
  const isPaymentDue = (day) => {
    return payments.some((payment) =>
      day.isSame(dayjs(payment.date_to_pay), "day")
    );
  };

  return (
    <div className="w-full h-full bg-white rounded-lg">
      {/* Header con botones de navegación */}
      <div className="p-5 dark:bg-white bg-white rounded-t">
        <div className="px-4 flex items-center justify-between">
          <span className="text-base font-bold text-gray-800">
            {currentDate.format("MMMM YYYY")}
          </span>
          <div className="flex items-center">
            <button onClick={handlePreviousMonth} className="text-gray-800">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="24"
                height="24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M15 18l-6-6 6-6" />
              </svg>
            </button>
            <button onClick={handleNextMonth} className="ml-3 text-gray-800">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="24"
                height="24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M9 18l6-6-6-6" />
              </svg>
            </button>
          </div>
        </div>

        {/* Tabla con los días del mes */}
        <div className="flex items-center justify-between pt-6 overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                {["Do", "Lu", "Mar", "Mi", "Ju", "Vi", "Sa"].map((day) => (
                  <th key={day}>
                    <div className="w-full flex justify-center">
                      <p className="text-base font-medium text-center text-gray-800">
                        {day}
                      </p>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {Array.from({ length: Math.ceil(days.length / 7) }, (_, i) => (
                <tr key={i}>
                  {days.slice(i * 7, i * 7 + 7).map((day, idx) => (
                    <td key={idx} className="">
                      <div className="p-1 cursor-pointer flex w-full justify-center">
                        {day.isSame(today, "day") ? (
                          // Día actual
                          <div className="w-full h-full">
                            <div className="flex items-center justify-center w-full rounded-full cursor-pointer">
                              <a
                                role="link"
                                tabIndex="0"
                                className="focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-700 focus:bg-indigo-500 hover:bg-indigo-500 text-base w-8 h-8 flex items-center justify-center font-medium text-white bg-indigo-700 rounded-full"
                              >
                                {day.format("D")}
                              </a>
                            </div>
                          </div>
                        ) : (
                          // Días normales
                          <p
                            className={`text-base ${
                              day.isSame(currentDate, "month")
                                ? "text-gray-500"
                                : "text-gray-300"
                            } ${isPaymentDue(day) ? "text-red-500" : ""}`}
                          >
                            {day.format("D")}
                          </p>
                        )}
                      </div>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recordatorios de pagos */}
      <div className="px-5 overflow-y-auto rounded-b">
  <Typography variant="h5" className="mb-4">Próximos pagos</Typography>
  <div className="px-4">
    {payments
      .filter((payment) =>
        currentDate.isSame(dayjs(payment.date_to_pay), "month")
      )
      .map((payment) => {
        const paymentDate = dayjs(payment.date_to_pay);
        const dayOfWeek = paymentDate.format("ddd"); // Día de la semana abreviado (e.g., "Mar")
        const month = paymentDate.format("MMMM"); // Nombre del mes completo (e.g., "Septiembre")
        const day = paymentDate.format("D"); // Día del mes (e.g., "1")

        return (
          <div key={payment.id} className="">
            <div className="flex items-center space-x-4 mb-4">
              {/* Círculo con el día */}
              <div className="w-10 h-10 flex items-center justify-center rounded-full bg-blue-500 text-white font-semibold">
                {day}
              </div>

              {/* Div con día y mes */}
              <div className="flex flex-col">
                <p className="text-sm font-medium text-gray-800">
                  {dayOfWeek}
                </p>
                <p className="text-xs font-light text-gray-500">
                  {month}
                </p>
              </div>
              
              {/* Lógica para mostrar el estado del pago */}
              <div className="ml-auto">
                {payment.paid ? (
                  <span className={`text-sm ${payment.paid_on_time ? 'text-green-500' : 'text-yellow-500'}`}>
                    {payment.paid_on_time ? 'Pagado a tiempo' : 'Pagado tarde'}
                  </span>
                ) : (
                  <span className="text-sm text-red-500">No pagado</span>
                )}
              </div>
            </div>
          </div>
        );
      })}
  </div>
</div>
    </div>
  );
};

export default Calendar;
