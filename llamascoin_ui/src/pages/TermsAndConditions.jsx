import React from "react";
import Layout from "../components/Layout"; 

export default function TermsAndConditions() {
return (
    <Layout>
    <section className="content1">
        <div className="terms-container">
        <h2 className="heading-t">Términos y Condiciones</h2>
        
        <p>
            Bienvenido a LlamasCoin.
        </p> 
        <br />
        <p>
            Al acceder o utilizar nuestro sitio web, aceptas cumplir y estar sujeto a los
            siguientes términos y condiciones y a cualquier cambio posterior realizado a los términos.
        </p>
        <br />

        <h3 style={{fontWeight: 'bolder'}}>1. Información General</h3>
        <br />
        <p>
            <strong>1.1. Descripción: </strong> LlamasCoin es un sitio web para conectar prestatarios y prestamistas de manera sencilla sin
            necesidad de una institución bancaria de por medio.
        </p>
        <br />
        <p>
            <strong>1.2. Cambios a los términos y condiciones:</strong> El Sitio web puede cambiar los Términos de Uso a su sola discreción. 
            El uso continuo de este sitio web después de la publicación de dichos cambios constituirá tu consentimiento a todos esos cambios. 
            Es tu responsabilidad revisar los Términos de Uso del sitio web para revisar la versión actual.
        </p>
        <br />

        <h3 style={{fontWeight: 'bolder'}}>2. Limitación de Responsabilidad</h3>
        <br />
        <p>
            <strong>2.1</strong> El uso de cualquier información o material en este sitio web es completamente bajo tu propio riesgo, por lo que
            no seremos responsables. Será tu responsabilidad asegurarte de que cualquier producto, servicio o información
            disponible a través de este sitio web cumpla con tus requisitos específicos.
        </p>
        <br />

        <h3 style={{fontWeight: 'bolder'}}>3. Propiedad Intelectual</h3>
        <br />
        <p>
            <strong>3.1</strong> Todos los contenidos presentes en este sitio web, incluidos textos, gráficos, logotipos, iconos, imágenes y software,
            son propiedad de LlamasCoin o de sus proveedores de contenido y están protegidos por las leyes de propiedad intelectual.
        </p>
        <br />

        <h3 style={{fontWeight: 'bolder'}}>4. Limitaciones en el Uso del Servicio</h3>
        <br />
        <p>
            <strong>4.1</strong> Al utilizar este sitio web, te comprometes a no utilizarlo para fines ilegales o no autorizados. 
            También aceptas no interferir con el funcionamiento de este sitio o intentar acceder a las áreas no autorizadas del mismo.
        </p>
        <br />

        <h3 style={{fontWeight: 'bolder'}}>5. Política de Privacidad</h3>
        <br />
        <p>
            <strong>5.1</strong> Consulta nuestra política de privacidad para obtener información detallada 
            sobre cómo recopilamos, usamos y protegemos tu información personal.
        </p>
        <br />

        <h3 style={{fontWeight: 'bolder'}}>6. Ley Aplicable</h3>
        <br />
        <p>
            <strong>6.1</strong> Estos términos y condiciones se interpretarán de acuerdo con las leyes de los Estados Unidos Mexicanos, 
            sin tener en cuenta las disposiciones sobre conflicto de leyes.
        </p>
        <br />
        </div>
    </section>
    </Layout>
);
}
