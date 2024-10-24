import React, { useState } from 'react';
import axios from 'axios';
import {Button} from '@material-tailwind/react'

export default function PaymentButton ()  {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handlePayment = async () => {
        setLoading(true);
        setError(null);
        try {
          
            const response = await axios.post('http://127.0.0.1:8000/paypal/create-payment/', {
                amount: '10.00', 
                currency: 'USD'
            });

            // Obtener los links de PayPal y redirigir al usuario
            const approvalUrl = response.data.links.find(link => link.rel === 'approval_url');
            if (approvalUrl) {
                window.location.href = approvalUrl.href; // Redirigir al URL de aprobación de PayPal
            } else {
                setError('No se pudo obtener la URL de aprobación de PayPal');
            }
        } catch (err) {
            console.error('Error al crear el pago:', err);
            setError('Hubo un error al crear el pago');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='flex min-h-10'>
            {loading ? (
                <p>Procesando pago...</p>
            ) : (
                <Button  onClick={handlePayment}>Pagar con PayPal</Button>
            )}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

