import React, { useState } from 'react';
import dayjs from 'dayjs';
import 'dayjs/locale/es'; // Importar el idioma español

// Establecer el idioma a español
dayjs.locale('es');
const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(dayjs());
  const today = dayjs(); // Día actual

  // Datos de pagos
  const payments = [
    {
      id: 1,
      number_of_pay: 1,
      date_to_pay: '2024-11-18',
      paid: false,
      paid_on_time: null,
      active_loan: 1,
    },
    {
      id: 2,
      number_of_pay: 2,
      date_to_pay: '2024-11-25',
      paid: false,
      paid_on_time: null,
      active_loan: 1,
    },
    {
      id: 3,
      number_of_pay: 3,
      date_to_pay: '2024-12-02',
      paid: false,
      paid_on_time: null,
      active_loan: 1,
    },
    {
        "id": 4,
        "number_of_pay": 4,
        "date_to_pay": "2024-12-09",
        "paid": false,
        "paid_on_time": null,
        "active_loan": 1
    },
    {
        "id": 5,
        "number_of_pay": 5,
        "date_to_pay": "2024-12-16",
        "paid": false,
        "paid_on_time": null,
        "active_loan": 1
    },
    {
        "id": 6,
        "number_of_pay": 6,
        "date_to_pay": "2024-12-23",
        "paid": false,
        "paid_on_time": null,
        "active_loan": 1
    },
    {
        "id": 7,
        "number_of_pay": 7,
        "date_to_pay": "2024-12-30",
        "paid": false,
        "paid_on_time": null,
        "active_loan": 1
    },
    {
        "id": 8,
        "number_of_pay": 8,
        "date_to_pay": "2025-01-06",
        "paid": false,
        "paid_on_time": null,
        "active_loan": 1
    },
    {
        "id": 9,
        "number_of_pay": 9,
        "date_to_pay": "2025-01-13",
        "paid": false,
        "paid_on_time": null,
        "active_loan": 1
    },
    {
        "id": 10,
        "number_of_pay": 10,
        "date_to_pay": "2025-01-20",
        "paid": false,
        "paid_on_time": null,
        "active_loan": 1
    },
  ];

  // Función para mover al mes anterior
  const handlePreviousMonth = () => {
    setCurrentDate(currentDate.subtract(1, 'month'));
  };

  // Función para mover al mes siguiente
  const handleNextMonth = () => {
    setCurrentDate(currentDate.add(1, 'month'));
  };

  // Generar las fechas del calendario del mes actual
  const generateCalendar = () => {
    const startOfMonth = currentDate.startOf('month');
    const endOfMonth = currentDate.endOf('month');
    const startDate = startOfMonth.startOf('week');
    const endDate = endOfMonth.endOf('week');

    let days = [];
    let day = startDate;

    // Generamos todos los días del mes actual, incluso los días que no pertenecen a este mes
    while (day.isBefore(endDate, 'day')) {
      days.push(day);
      day = day.add(1, 'day');
    }
    return days;
  };

  const days = generateCalendar();

  // Función para verificar si un día tiene un pago programado
  const isPaymentDue = (day) => {
    return payments.some((payment) => day.isSame(dayjs(payment.date_to_pay), 'day'));
  };

  return (
    <div className="max-w-sm w-full shadow-lg">
      {/* Header con botones de navegación */}
      <div className="md:p-8 p-5 dark:bg-gray-800 bg-white rounded-t">
        <div className="px-4 flex items-center justify-between">
          <span className="text-base font-bold dark:text-gray-100 text-gray-800">
            {currentDate.format('MMMM YYYY')}
          </span>
          <div className="flex items-center">
            <button onClick={handlePreviousMonth} className="text-gray-800 dark:text-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M15 18l-6-6 6-6" />
              </svg>
            </button>
            <button onClick={handleNextMonth} className="ml-3 text-gray-800 dark:text-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 18l6-6-6-6" />
              </svg>
            </button>
          </div>
        </div>

        {/* Tabla con los días del mes */}
        <div className="flex items-center justify-between pt-12 overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                {['Do', 'Lu', 'Mar', 'Mi', 'Ju', 'Vi', 'Sa'].map((day) => (
                  <th key={day}>
                    <div className="w-full flex justify-center">
                      <p className="text-base font-medium text-center text-gray-800 dark:text-gray-100">
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
                    <td key={idx} className="pt-6">
                      <div className="px-2 py-2 cursor-pointer flex w-full justify-center">
                        {day.isSame(today, 'day') ? (
                          // Día actual
                          <div className="w-full h-full">
                            <div className="flex items-center justify-center w-full rounded-full cursor-pointer">
                              <a
                                role="link"
                                tabIndex="0"
                                className="focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-700 focus:bg-indigo-500 hover:bg-indigo-500 text-base w-8 h-8 flex items-center justify-center font-medium text-white bg-indigo-700 rounded-full"
                              >
                                {day.format('D')}
                              </a>
                            </div>
                          </div>
                        ) : (
                          // Días normales
                          <p
                            className={`text-base ${day.isSame(currentDate, 'month') ? 'text-gray-500 dark:text-gray-100' : 'text-gray-300'} ${isPaymentDue(day) ? 'text-red-500' : ''}`}
                          >
                            {day.format('D')}
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
      <div className="md:py-8 py-5 md:px-16 px-5 dark:bg-gray-700 bg-gray-50 rounded-b">
        <div className="px-4">
          {payments.filter((payment) => currentDate.isSame(dayjs(payment.date_to_pay), 'month')).map((payment) => (
            <div key={payment.id} className="border-b pb-4 border-gray-400 border-dashed">
              <p className="text-xs font-light leading-3 text-gray-500 dark:text-gray-300">
                {new Date(payment.date_to_pay).toLocaleString('es-US', {
                  hour: '2-digit',
                  minute: '2-digit',
                  hour12: true,
                })}
              </p>
              <a
                tabIndex="0"
                className="focus:outline-none text-lg font-medium leading-5 text-gray-800 dark:text-gray-100 mt-2"
              >
                Pago {payment.number_of_pay}: Se vence el{' '}
                {new Date(payment.date_to_pay).toLocaleDateString()}
              </a>

            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Calendar;
