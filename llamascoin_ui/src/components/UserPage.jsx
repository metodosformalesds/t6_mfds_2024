import React from 'react';
import { Card, Input, Typography } from "@material-tailwind/react";
import { useFetch } from '../hooks/useFetch';
import { apiHost } from '../utils/apiconfig';
import { useAuth } from '../context/AuthContext';
import { ProfileCard } from './ProfileCard';

export default function UserAccount() {
  const { authData } = useAuth();
  const { status: userStatus, data: userData } = useFetch(apiHost + "user/" + authData.userId);

  if (userStatus !== 'success') {
    return <div>Loading...</div>; 
  }

  return (
    <Card className="p-12 mx-12 shadow-xl w-full shadow-blue-gray-900/">
      <Typography variant="h3" color="blue-gray" className="mb-6">
        Cuenta
      </Typography>
      <div className="grid grid-cols-3 gap-8">
        <Card className="flex flex-col space-y-4 p-6">
          <ProfileCard entity={userData} />
          <div>
            <Typography variant="h6" color="blue-gray">
              Fecha de Nacimiento
            </Typography>
            <Input value={userData.birth_date}  />
          </div>
          <div>
            <Typography variant="h6" color="blue-gray">
              Teléfono
            </Typography>
            <Input value={userData.phone_number}  />
          </div>
        </Card>

        <Card className="col-span-2 space-y-4 p-6">
          <div>
            <Typography variant="h6" color="blue-gray">
              Dirección Completa
            </Typography>
            <Input value={userData.full_address} />
          </div>
          <div>
            <Typography variant="h6" color="blue-gray">
              Ciudad
            </Typography>
            <Input value={userData.city}/>
          </div>
          <div>
            <Typography variant="h6" color="blue-gray">
              Barrio
            </Typography>
            <Input value={userData.neighborhood} />
          </div>
          <div>
            <Typography variant="h6" color="blue-gray">
              Código Postal
            </Typography>
            <Input value={userData.postal_code}  />
          </div>
          <div>
            <Typography variant="h6" color="blue-gray">
              Estado
            </Typography>
            <Input value={userData.state}  />
          </div>
          <div>
            <Typography variant="h6" color="blue-gray">
              Municipio
            </Typography>
            <Input value={userData.municipality}  />
          </div>
          <div>
            <Typography variant="h6" color="blue-gray">
              Nacionalidad
            </Typography>
            <Input value={userData.nationality}  />
          </div>
        </Card>
      </div>
    </Card>
  );
}
