import {
  Card,
  CardHeader,
  CardBody,
  Typography,
  Avatar,
} from "@material-tailwind/react";
import defaultImg from '../assets/images/profileCard.webp';

export function ProfileCard({ entity }) {
  if (!entity) {
      return (
          <Card color="transparent" shadow={false} className="flex justify-center items-center h-full">
              <Typography variant="h6" color="blue-gray">
                  Cargando...
              </Typography>
          </Card>
      );
  }

  return (
      <Card color="transparent" shadow={false}>
          <CardHeader
              color="transparent"
              floated={false}
              shadow={false}
              className="mx-0 flex items-center gap-4 pt-0"
          >
              <Avatar
                  size="lg"
                  variant="circular"
                  src={defaultImg}
                  alt={entity.first_name || 'Avatar'}
              />
              <div className="flex w-full flex-col gap-0.5">
                  <div className="flex items-center justify-between">
                      <Typography variant="h5" color="blue-gray">
                          {entity.first_name + " " + entity.first_surname}
                      </Typography>
                      <div className="flex items-center gap-0">
                      </div>
                  </div>
                  <Typography color="blue-gray">{entity.rfc}</Typography>
              </div>
          </CardHeader>
      </Card>
  );
}
