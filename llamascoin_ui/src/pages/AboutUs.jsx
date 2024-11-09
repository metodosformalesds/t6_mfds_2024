import React from "react";
import Layout from "../components/Layout"; 

export default function AboutUs() {
  return (
    <Layout>
      <section className="content1">
        <div className="about-container">
          <h2 className="heading-t">Acerca de Nosotros</h2>
          
          <p>
            Bienvenido a LlamasCoin, tu plataforma electrónica de préstamos personales en México. 
            Nuestra misión es conectar a prestamistas que buscan hacer crecer su capital cobrando intereses justos 
            con prestatarios que necesitan capital para cubrir necesidades específicas. A través de LlamasCoin, 
            ofrecemos una solución simple y segura para facilitar este proceso.
          </p> 
          <br />
          
          <h3 style={{fontWeight: 'bolder'}}>Nuestra Plataforma</h3>
          <br />
          <p>
            En LlamasCoin, permitimos a los prestamistas publicar sus ofertas de préstamos con montos, tasas de interés, 
            y plazos de pago específicos, de modo que los prestatarios pueden seleccionar la opción que mejor se adapte 
            a sus necesidades. Nos encargamos de realizar las transacciones bancarias correspondientes, dando formalidad 
            y seguridad a cada préstamo.
          </p>
          <br />

          <h3 style={{fontWeight: 'bolder'}}>Cumplimiento y Regulación</h3>
          <br />
          <p>
            LlamasCoin cumple con la ley fintech de México y las regulaciones establecidas por el Banco de México. 
            Actualmente, las tasas de interés están limitadas a un máximo de 22.75%, con un Costo Anual Total (CAT) del 28.18%, 
            según el Banco de México en julio de 2024. Todas las regulaciones se actualizarán conforme a los cambios 
            indicados por las instituciones financieras mexicanas, y serán gestionadas por nuestro equipo administrativo.
          </p>
          <br />

          <h3 style={{fontWeight: 'bolder'}}>Compromiso con la Transparencia y la Seguridad</h3>
          <br />
          <p>
            En LlamasCoin, creemos en la importancia de la transparencia y la seguridad. Registramos las fechas de pagos, 
            saldos y posibles atrasos de manera detallada, y facilitamos el proceso de pago para los prestatarios. 
            Además, protegemos rigurosamente la información sensible de todos nuestros usuarios, asegurando un ambiente seguro 
            para realizar todas las transacciones.
          </p>
          <br />

          <h3 style={{fontWeight: 'bolder'}}>Tu Crecimiento Financiero</h3>
          <br />
          <p>
            A medida que los prestatarios cumplen puntualmente con sus pagos, tienen la oportunidad de mejorar su puntaje crediticio 
            y aumentar el monto de su línea de crédito. Esto fomenta una relación de confianza y crecimiento financiero, apoyando 
            la economía local y promoviendo un sistema de financiamiento más accesible para todos.
          </p>
          <br />
        </div>
      </section>
    </Layout>
  );
}
