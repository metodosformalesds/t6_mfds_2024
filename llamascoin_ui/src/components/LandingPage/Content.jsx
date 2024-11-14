import "../LandingPage/css.css";
import {
  FaUserAlt,
  FaHandHoldingUsd,
  FaMoneyBillWave,
  FaCreditCard,
} from "react-icons/fa";
import Paypal from "../../assets/landingpage/paypal_icon.png";
import Buro from "../../assets/landingpage/moffin.png";
import ima1 from "../../assets/landingpage/ima1.jpg";
import ima2 from "../../assets/landingpage/ganar2.png";
import ima3 from "../../assets/landingpage/Prestardinero.jpg";
import ima4 from "../../assets/landingpage/noso.jpg";
import ima5 from "../../assets/landingpage/procesosfin.jpg";
import ima6 from "../../assets/landingpage/Responsabilidad Financiera.jpg";
import ima7 from "../../assets/landingpage/innovación.jpg";
import ima8 from "../../assets/landingpage/confianza.jpg";

import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
  Button,
} from "@material-tailwind/react";
export function ContentDesign() {
  return (
    <section className="content1">
      <div className="sección-cont">
        <h2 className="heading-t">
          {" "}
          Nuestros <span className="span">Clientes</span>
        </h2>
        <h2 className="subtext">Algunos de nuestros socios</h2>
        <div className="columns-2 ...">
          <img src={Buro} className="image-paragraph"></img>
          <img src={Paypal} className="image-paragraph"></img>
        </div>
      </div>
      <div className="sección-cont">
        <h2 className="heading-t">
          {" "}
          Gestiona tus préstamos y oportunidades de inversión en{" "}
          <span className="span">un solo lugar</span>
        </h2>
        <h2 className="subtext">¿A quien está dirigida nuestra plataforma?</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
          <Card className="mt-6 w-full max-w-sm mx-auto shadow-lg">
            <CardHeader color="blue-gray" className="relative h-56">
              <img
                src={ima1}
                alt="card-image"
                className="object-cover h-full w-full"
              />
            </CardHeader>
            <CardBody>
              <Typography variant="h5" color="blue-gray" className="mb-2">
                Personas interesadas en invertir
              </Typography>
              <Typography className="text-gray-700">
                Conviértete en prestamista y haz crecer tu dinero con tasas
                competitivas. Automatizamos pagos y monitoreo de tus inversiones
              </Typography>
            </CardBody>
            <CardFooter className="pt-2"></CardFooter>
          </Card>

          <Card className="mt-6 w-full max-w-sm mx-auto shadow-lg">
            <CardHeader color="blue-gray" className="relative h-56">
              <img
                src={ima2}
                alt="card-image"
                className="object-cover h-full w-full"
              />
            </CardHeader>
            <CardBody>
              <Typography variant="h5" color="blue-gray" className="mb-2">
                Personas que necesitan un préstamo
              </Typography>
              <Typography className="text-gray-700">
                Obtén préstamos rápidos y fáciles sin pasar por bancos. Elige
                entre diversas opciones de créditos según tus necesidades.
              </Typography>
            </CardBody>
            <CardFooter className="pt-2"></CardFooter>
          </Card>

          <Card className="mt-6 w-full max-w-sm mx-auto shadow-lg">
            <CardHeader color="blue-gray" className="relative h-56">
              <img
                src={ima3}
                alt="card-image"
                className="object-cover h-full w-full"
              />
            </CardHeader>
            <CardBody>
              <Typography variant="h5" color="blue-gray" className="mb-2">
                Emprendedores y trabajadores independientes
              </Typography>
              <Typography className="text-gray-700">
                Accede a créditos flexibles para impulsar tu crecimiento, con
                total seguridad y formalidad en cada transacción.
              </Typography>
            </CardBody>
            <CardFooter className="pt-2"></CardFooter>
          </Card>
        </div>
      </div>
      <div className="sección-cont">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
          <div className="flex flex-col justify-center">
            <h2 className="text-2xl font-bold mb-4">
              El impacto de estar con nosotros
            </h2>
            <p className="text-gray-700 mb-4">
              Pasar tiempo en nuestra plataforma te permite mejorar tu salud
              financiera, ya sea como prestamista o prestatario. Con una
              comunidad en constante crecimiento, ofrecemos soluciones
              personalizadas que se adaptan a tus necesidades económicas,
              ayudándote a alcanzar tus metas financieras de manera eficiente y
              segura. ¡Forma parte de esta transformación!
            </p>
            <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">
              Mas información
            </button>
          </div>
          <div className="flex justify-center">
            <img src={ima4} className="object-cover w-full h-80 rounded-md" />
          </div>
        </div>
      </div>
      <div className="sectión-cont">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 custom-bg">
          <div className="flex justify-center">
            <img src={ima3} className="object-cover w-full h-80 rounded-md" />
          </div>

          <div className="flex flex-col justify-center">
            <h2 className="text-2xl font-bold mb-4 custom-text-color">
              Como ajustar su préstamo
            </h2>

            <p className="text-gray-700 mb-4 custom-text-color">
              Personaliza tu préstamo fácilmente. Selecciona el monto que
              necesitas, ajusta la tasa de interés y elige el plazo de pago que
              mejor se adapte a tu situación. Nuestra plataforma te permite
              comparar opciones de prestamistas para encontrar las mejores
              condiciones de manera rápida y sencilla. ¡Toma el control de tus
              finanzas en pocos pasos!
            </p>
            <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">
              Mas información
            </button>
          </div>
        </div>
      </div>
      <div className="sección-cont">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
          <div className="flex flex-col justify-center">
            <h2 className="text-2xl font-bold mb-4">
              Han confiado en nosotros
            </h2>
            <p className="text-gray-700 mb-4">
              "Necesitaba dinero urgente para cubrir unos gastos médicos
              inesperados. Con esta app, el proceso fue sencillo, y en menos de
              24 horas tenía el dinero en mi cuenta. Los plazos de pago son
              flexibles, y la atención al cliente es de primera. Me salvó en un
              momento de necesidad."
            </p>
            <button  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">
              Registrate
            </button>
          </div>
          <div className="flex justify-center">
            <img src={ima8} className="object-cover w-full h-80 rounded-md" />
          </div>
        </div>
      </div>
      <div className="sección-cont">
        <div className="stats-section py-12">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">
              Hemos llegado hasta aquí con esfuerzo y dedicación
            </h2>
          </div>

          <div className="mt-10 max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 text-center">
            <div>
              <FaUserAlt className="text-blue-500 mx-auto text-5xl mb-2" />
              <div className="text-4xl font-bold text-gray-900">2,245,341</div>
              <div className="text-gray-500 mt-2">Personas registradas</div>
            </div>
            <div>
              <FaHandHoldingUsd className="text-blue-500 mx-auto text-5xl mb-2" />
              <div className="text-4xl font-bold text-gray-900">46,328</div>
              <div className="text-gray-500 mt-2">Préstamos otorgados</div>
            </div>
            <div>
              <FaMoneyBillWave className="text-blue-500 mx-auto text-5xl mb-2" />
              <div className="text-4xl font-bold text-gray-900">828,867</div>
              <div className="text-gray-500 mt-2">Pagos procesados</div>
            </div>
            <div>
              <FaCreditCard className="text-blue-500 mx-auto text-5xl mb-2" />
              <div className="text-4xl font-bold text-gray-900">1,926,436</div>
              <div className="text-gray-500 mt-2">Préstamos generados</div>
            </div>
          </div>
        </div>
      </div>

      <div className="sección-cont">
        <h2 className="heading-t">
          {" "}
          El <span className="span">cuidado</span> es el nuevo <span>Marketing</span>
        </h2>
        <h2 className="subtext">
          Nuestro blog es el mejor lugar para estar al día sobre tendencias
          financieras y nuevas oportunidades. Descubre cómo nuestros usuarios
          están aprovechando la plataforma para aumentar sus ingresos y mejorar
          su bienestar económico.
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
          <Card className="mt-6 w-full max-w-sm mx-auto shadow-lg flex flex-col justify-between">
            <div>
              <CardHeader color="blue-gray" className="relative h-56">
                <img
                  src={ima5}
                  alt="card-image"
                  className="object-cover h-full w-full"
                />
              </CardHeader>
              <CardBody className="flex-grow">
                <Typography variant="h5" color="blue-gray" className="mb-2">
                  Creando procesos financieros seguros
                </Typography>
              </CardBody>
            </div>
          
          </Card>

          <Card className="mt-6 w-full max-w-sm mx-auto shadow-lg flex flex-col justify-between">
            <div>
              <CardHeader color="blue-gray" className="relative h-56">
                <img
                  src={ima6}
                  alt="card-image"
                  className="object-cover h-full w-full"
                />
              </CardHeader>
              <CardBody className="flex-grow">
                <Typography variant="h5" color="blue-gray" className="mb-2">
                  ¿Cuáles son tus responsabilidades financieras y cómo
                  gestionarlas?
                </Typography>
              </CardBody>
            </div>
           
          </Card>

          <Card className="mt-6 w-full max-w-sm mx-auto shadow-lg flex flex-col justify-between">
            <div>
              <CardHeader color="blue-gray" className="relative h-56">
                <img
                  src={ima7}
                  alt="card-image"
                  className="object-cover h-full w-full"
                />
              </CardHeader>
              <CardBody className="flex-grow">
                <Typography variant="h5" color="blue-gray" className="mb-2">
                  Innovando el modelo de préstamos con nuestra plataforma
                </Typography>
              </CardBody>
            </div>
          
          </Card>
        </div>
      </div>
    </section>
  );
}
