import React from "react";
import { Card, CardBody, Typography, CardFooter, Button } from "@material-tailwind/react";

const CardDashboard = ({ title, icon: Icon, iconColor, value }) => {
  return (
    <Card className="p-1">
      <CardBody>
        <div className=" items-center mb-4">
         
          <div className="flex justify-between items-center">
            <Typography  variant="h5"
                    color="blue-gray"
                    className="font-normal leading-none opacity-70">
              {title}
            </Typography>
            <Icon className={`h-12 w-12 ${iconColor}`} />
          </div>
            <Typography variant="h4" className="text-gray-900">
              {value}
            </Typography>
        </div>
      </CardBody>

    </Card>
  );
};

export default CardDashboard;
