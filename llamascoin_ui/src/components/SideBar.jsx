import { useState } from "react";
import { Card, Typography, List, ListItem, ListItemPrefix } from "@material-tailwind/react";
import { FaHome, FaClipboardList, FaUserCircle, FaCog, FaSignOutAlt, FaMoneyBill, FaMoneyBillWave } from "react-icons/fa";
import { useAuth } from "../context/AuthContext";

export function Sidebar({ onSelect }) {
  const { authData, logout } = useAuth();
  const role = authData?.role;

  const [activeItem, setActiveItem] = useState(role === 'borrower' ? 'loans' : 'dashboard');


  const handleSelect = (component) => {
    setActiveItem(component); // Establece el elemento activo
    onSelect(component);
  };

  return (
    <Card className="h-[calc(100vh-2rem)] w-full max-w-[20rem] p-4 shadow-xl shadow-blue-gray-900/5">
      <div className="flex">
        <a href="/" className="-m-1.5 p-1.5">
          <span className="sr-only">LlamasCoin</span>
          <img alt="" src="/images/Logo_l.png" className="h-10 w-auto" />
        </a>
      </div>
      <List>
        {role === 'borrower' && (
          <>
            <ListItem
              className={`cursor-pointer ${
                activeItem === 'loans' ? 'bg-blue-100' : ''
              }`}
              onClick={() => handleSelect('loans')}
            >
              <ListItemPrefix>
                <FaHome className="h-5 w-5" />
              </ListItemPrefix>
              Inicio
            </ListItem>
            <ListItem
              className={`cursor-pointer ${
                activeItem === 'creditHistory' ? 'bg-blue-100' : ''
              }`}
              onClick={() => handleSelect('creditHistory')}
            >
              <ListItemPrefix>
                <FaClipboardList className="h-5 w-5" />
              </ListItemPrefix>
              Historial crediticio
            </ListItem>
            <ListItem
              className={`cursor-pointer ${
                activeItem === 'loanHistory' ? 'bg-blue-100' : ''
              }`}
              onClick={() => handleSelect('loanHistory')}
            >
              <ListItemPrefix>
                <FaMoneyBill className="h-5 w-5" />
              </ListItemPrefix>
              Historial de préstamos
            </ListItem>
            <ListItem
              className={`cursor-pointer ${
                activeItem === 'account' ? 'bg-blue-100' : ''
              }`}
              onClick={() => handleSelect('account')}
            >
              <ListItemPrefix>
                <FaUserCircle className="h-5 w-5" />
              </ListItemPrefix>
              Cuenta
            </ListItem>
          </>
        )}
        {role === 'moneylender' && (
          <>
            <ListItem
              className={`cursor-pointer ${
                activeItem === 'dashboard' ? 'bg-blue-100' : ''
              }`}
              onClick={() => handleSelect('dashboard')}
            >
              <ListItemPrefix>
                <FaHome className="h-5 w-5" />
              </ListItemPrefix>
              Inicio
            </ListItem>
            <ListItem
              className={`cursor-pointer ${
                activeItem === 'loanHistory' ? 'bg-blue-100' : ''
              }`}
              onClick={() => handleSelect('loanHistory')}
            >
              <ListItemPrefix>
                <FaMoneyBill className="h-5 w-5" />
              </ListItemPrefix>
              Historial de préstamos
            </ListItem>
            <ListItem
              className={`cursor-pointer ${
                activeItem === 'myLoans' ? 'bg-blue-100' : ''
              }`}
              onClick={() => handleSelect('myLoans')}
            >
              <ListItemPrefix>
                <FaMoneyBillWave className="h-5 w-5" />
              </ListItemPrefix>
              Mis préstamos
            </ListItem>
            <ListItem
              className={`cursor-pointer ${
                activeItem === 'account' ? 'bg-blue-100' : ''
              }`}
              onClick={() => handleSelect('account')}
            >
              <ListItemPrefix>
                <FaUserCircle className="h-5 w-5" />
              </ListItemPrefix>
              Cuenta
            </ListItem>
          </>
        )}
        <ListItem onClick={logout}>
          <ListItemPrefix>
            <FaSignOutAlt className="h-5 w-5" />
          </ListItemPrefix>
          Cerrar Sesión
        </ListItem>
      </List>
    </Card>
  );
}
