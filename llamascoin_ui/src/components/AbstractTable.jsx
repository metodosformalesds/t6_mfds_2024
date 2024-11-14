import { useEffect, useState } from "react";
import { Card, CardBody, CardHeader, Typography } from "@material-tailwind/react";
import { useFetch } from "../hooks/useFetch";
import { getAmountColor } from "../utils/amountColor";
import { useAuth } from "../context/AuthContext";
export function AbstractTable({ tableHeaders, apiUrl, title }) {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { status, data } = useFetch(apiUrl);
  const {authData} = useAuth();
  useEffect(() => {
    if (status === "success" && data) {
    
      setRows(data);
      setLoading(false);
    } else if (status === "error") {
      console.error("Error fetching data: ", status);
      setError("Error al cargar los datos");
    }
  }, [status, data]);

  if (loading) {
    return <Typography color="gray">Cargando datos...</Typography>;
  }

  if (error) {
    return <Typography color="red">{error}</Typography>;
  }

  return (
    <Card className="h-full w-full shadow-none">
      <CardHeader floated={false} shadow={false} className="rounded-none">
        <div className="mb-4 flex flex-col justify-between gap-8 md:flex-row md:items-center">
          <Typography variant="h5" color="blue-gray">
            {title}
          </Typography>
        </div>
      </CardHeader>
      <CardBody className="px-0 max-h-[200px] overflow-y-auto">
      {rows.length === 0 ? (
          <div className="text-center"><Typography color="gray">No hay más registros</Typography></div>
        ) : (
          <table className="text-left">
            <thead>
              <tr>
                {Object.keys(tableHeaders).map((header) => (
                  <th
                    key={header}
                    className="border-y border-blue-gray-100 bg-blue-gray-50/50 p-4"
                  >
                    <Typography
                      variant="small"
                      color="blue-gray"
                      className="font-normal leading-none opacity-70"
                    >
                      {header}
                    </Typography>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {Object.entries(tableHeaders).map(([header, key], cellIndex) => (
                    <td key={cellIndex} className="p-4 border-b border-blue-gray-50">
                      <Typography variant="small" color="blue-gray" className="font-normal">
                      {key === "person" ? (
                          <>
                            {row[key]?.first_name} {row[key]?.first_surname} {row[key]?.second_surname}
                          </>
                        ) : (
                          key === "amount_paid" ? (
                            <span className={getAmountColor(row.transaction_type, authData?.role)}>
                              {row[key]} MXN
                            </span>
                          ) : (
                            row[key]
                          )
                        )}
               
                      </Typography>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </CardBody>
    </Card>
  );
}
