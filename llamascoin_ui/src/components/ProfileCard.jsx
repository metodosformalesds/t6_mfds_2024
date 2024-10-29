import {
    Card,
    CardHeader,
    CardBody,
    Typography,
    Avatar,
  } from "@material-tailwind/react";
import defaultImg from '../assets/images/profileCard.webp'
   
  export function ProfileCard({entity}) {
    return (
      <Card color="transparent" shadow={false} className=" ">
        <CardHeader
          color="transparent"
          floated={false}
          shadow={false}
          className="mx-0 flex items-center gap-4 pt-0 "
        >
          {/* <Avatar
            size="lg"
            variant="circular"
            src={defaultImg}
            alt={entity}
          /> */}
          <div className="flex w-full flex-col gap-0.5">
            <div className="flex items-center justify-between">
              <Typography variant="h5" color="blue-gray">
                {entity}
              </Typography>
              <div className="5 flex items-center gap-0">

              </div>
            </div>
            <Typography color="blue-gray">{entity.rfc}</Typography>
          </div>
        </CardHeader>

      </Card>
    );
  }