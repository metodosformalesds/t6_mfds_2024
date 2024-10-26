import { Link, useLocation } from "react-router-dom";
import { Card, Typography, List, ListItem, ListItemPrefix } from "@material-tailwind/react";
import { FaHome, FaClipboardList, FaUserCircle, FaCog, FaSignOutAlt } from "react-icons/fa"; // Importar iconos de react-icons
import { useAuth } from "../context/AuthContext";
export function Sidebar() {
  const { authData, logout} = useAuth();
  const role = authData?.role;
  const location = useLocation(); 

  return (
    <Card className=" h-[calc(100vh-2rem)] w-full max-w-[20rem] p-4 shadow-xl shadow-blue-gray-900/5">
        <div className="flex ">
          <a href="/" className="-m-1.5 p-1.5">
            <span className="sr-only">LlamasCoin</span>
            <img
              alt=""
              src="/images/Logo_l.png"
              className="h-10 w-auto"
            />
          </a>
        </div>
      <List>
        {role === 'borrower' && (
          <>
            <ListItem className={location.pathname === '/home' ? 'bg-blue-200' : ''}>
              <ListItemPrefix>
                <FaHome className="h-5 w-5" />
              </ListItemPrefix>
              <Link to="/" className="flex items-center w-full h-full text-left">
                Inicio
              </Link>
            </ListItem>
            <ListItem className={location.pathname === '/credit-history' ? 'bg-blue-200' : ''}>
              <ListItemPrefix>
                <FaClipboardList className="h-5 w-5" />
              </ListItemPrefix>
              <Link to="/credit-history" className="flex items-center w-full h-full text-left">
                Historial Crediticio
              </Link>
            </ListItem>
            <ListItem className={location.pathname === '/account' ? 'bg-blue-200' : ''}>
              <ListItemPrefix>
                <FaUserCircle className="h-5 w-5" />
              </ListItemPrefix>
              <Link to="/account" className="flex items-center w-full h-full text-left">
                Cuenta
              </Link>
            </ListItem>
          </>
        )}
        {role === 'moneylender' && (
          <>
            <ListItem className={location.pathname === '/home' ? 'bg-blue-200' : ''}>
              <ListItemPrefix>
                <FaHome className="h-5 w-5" />
              </ListItemPrefix>
              <Link to="/" className="flex items-center w-full h-full text-left">
                Inicio
              </Link>
            </ListItem>
            <ListItem className={location.pathname === '/subscription' ? 'bg-blue-200' : ''}>
              <ListItemPrefix>
                <FaClipboardList className="h-5 w-5" />
              </ListItemPrefix>
              <Link to="/my-subscription" className="flex items-center w-full h-full text-left">
                Suscripción
              </Link>
            </ListItem>
            <ListItem className={location.pathname === '/account' ? 'bg-blue-200' : ''}>
              <ListItemPrefix>
                <FaUserCircle className="h-5 w-5" />
              </ListItemPrefix>
              <Link to="/account" className="flex items-center w-full h-full text-left">
                Cuenta
              </Link>
            </ListItem>
          </>
        )}
        <ListItem className={location.pathname === '/logout' ? 'bg-blue-200' : ''}>
          <ListItemPrefix>
            <FaSignOutAlt className="h-5 w-5" />
          </ListItemPrefix>
          <Link to="/" onClick={()=>logout()} className="flex items-center w-full h-full text-left">
            Cerrar Sesión
          </Link>
        </ListItem>
      </List>
    </Card>
  );
}
