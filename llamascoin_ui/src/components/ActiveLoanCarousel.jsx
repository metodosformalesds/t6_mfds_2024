import React from 'react';
import { ProfileCard } from './ProfileCard';
import Calendar from './calendar';
import { Typography, IconButton,  } from '@mui/material';
import { Carousel, Card } from '@material-tailwind/react';

const ActiveLoanCarousel = ({ activeLoans }) => {
  return (
     <Carousel
      className="rounded-xl h-96 w-full"
      prevArrow={({ handlePrev }) => (
        <IconButton
          variant="text"
          color="white"
          size="lg"
          onClick={handlePrev}
          className="!absolute bottom-4 left-4 -translate-y-2/4 bg-blue-500 hover:bg-blue-700 text-white rounded-full p-2 shadow-md"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="h-6 w-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18"
            />
          </svg>
        </IconButton>
      )}
      nextArrow={({ handleNext }) => (
        <IconButton
          variant="text"
          color="white"
          size="lg"
          onClick={handleNext}
          className="!absolute bottom-4 right-4 -translate-y-2/4 bg-blue-500 hover:bg-blue-700 text-white rounded-full p-2 shadow-md"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="h-6 w-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
            />
          </svg>
        </IconButton>
      )}
    >
      {Array.isArray(activeLoans) &&
        activeLoans.map((loan) => (
          <div
            key={loan.id}
            className="items-center  bg-white rounded-md shadow-md"
          >
            {/* ProfileCard */}
            <ProfileCard entity={loan.borrower} />

            {/* Loan Info */}
            <div className="mt-4 text-center">
              <Typography variant="h6" component="p" color="textPrimary">
                Monto total:{' '}
                <Typography component="span" color="success.main">
                  ${loan.loan_amount}
                </Typography>
              </Typography>
              <Typography variant="body1" color="textSecondary" className='b'>
                Pagado:{' '}
                <Typography component="span" color="primary.main">
                  ${loan.total_debt_paid}
                </Typography>
              </Typography>
              <Typography variant="body1" color="textSecondary">
                Por pagar:{' '}
                <Typography component="span" color="error.main">
                  ${loan.amount_to_pay}
                </Typography>
              </Typography>
              <Typography variant="body1" color="textSecondary">
                Fecha de inicio: {loan.start_date}
              </Typography>
            </div>

            {/* Calendar */}
            <div className="mt-4">
              <Calendar payments={loan.payments} />
            </div>
          </div>
        ))}
    </Carousel>
  );
};

export default ActiveLoanCarousel;
