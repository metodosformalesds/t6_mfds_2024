import { useState } from "react";
import { Card, Typography, List, ListItem, ListItemPrefix } from "@material-tailwind/react";
import { FaHome, FaClipboardList, FaUserCircle, FaCog, FaSignOutAlt } from "react-icons/fa";
import { useAuth } from "../context/AuthContext";

export function Sidebar({ onSelect }) {
  const { authData, logout } = useAuth();
  const role = authData?.role;

  const handleSelect = (component) => {
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
            <ListItem onClick={() => handleSelect('loans')}>
              <ListItemPrefix>
                <FaHome className="h-5 w-5" />
              </ListItemPrefix>
              Inicio
            </ListItem>
            <ListItem onClick={() => handleSelect('creditHistory')}>
              <ListItemPrefix>
                <FaClipboardList className="h-5 w-5" />
              </ListItemPrefix>
              Historial Crediticio
            </ListItem>
            <ListItem onClick={() => handleSelect('account')}>
              <ListItemPrefix>
                <FaUserCircle className="h-5 w-5" />
              </ListItemPrefix>
              Cuenta
            </ListItem>
          </>
        )}
        {role === 'moneylender' && (
          <>
            <ListItem onClick={() => handleSelect('dashboard')}>
              <ListItemPrefix>
                <FaHome className="h-5 w-5" />
              </ListItemPrefix>
              Inicio
            </ListItem>

            <ListItem onClick={() => handleSelect('account')}>
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
