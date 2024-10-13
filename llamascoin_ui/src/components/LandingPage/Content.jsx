import '../LandingPage/css.css';
import Stripe from '../../assets/landingpage/stripe.png'
import Buro from '../../assets/landingpage/buro.png'
import ima1 from '../../assets/landingpage/ima1.jpg'
import ima2 from '../../assets/landingpage/ganar2.png'
import ima3 from '../../assets/landingpage/Prestardinero.jpg'
import ima4 from '../../assets/landingpage/noso.jpg'
import {Card,CardHeader,CardBody,CardFooter,Typography,Button,} from "@material-tailwind/react";
export function ContentDesign() {
    return(
        <section class="content1">
            <div class="sección-cont">
                <h2 class="heading-t"> Nuestros  <span>Clientes</span></h2>
                <h2 class="subtext">Algunos de nuestros socios</h2>
                <div class="columns-2 ...">
                <img src={Buro} class="image-paragraph"></img>
                <img src={Stripe} class="image-paragraph"></img>
                </div>
            </div>
            <div class="sección-cont">
                <h2 class="heading-t"> Gestiona tus préstamos y oportunidades de inversión en <span>un solo lugar</span></h2> 
                <h2 class="subtext">¿A quien está dirigida nuestra plataforma?</h2>
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
                                Conviértete en prestamista y haz crecer tu dinero con tasas competitivas. Automatizamos pagos y monitoreo de tus inversiones
                            </Typography>
                            </CardBody>
                            <CardFooter className="pt-2">
                            </CardFooter>
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
                            Obtén préstamos rápidos y fáciles sin pasar por bancos. Elige entre diversas opciones de créditos según tus necesidades.
                        </Typography>
                        </CardBody>
                        <CardFooter className="pt-2">
                        </CardFooter>
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
                            Accede a créditos flexibles para impulsar tu crecimiento, con total seguridad y formalidad en cada transacción.
                        </Typography>
                        </CardBody>
                        <CardFooter className="pt-2">
                        </CardFooter>
                    </Card>
                </div>
            </div>
            <div class="sección-cont">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
                    <div className="flex flex-col justify-center">
                        <h2 className="text-2xl font-bold mb-4">El impacto de estar con nosotros</h2>
                        <p className="text-gray-700 mb-4">
                        Pasar tiempo en nuestra plataforma te permite mejorar tu salud financiera, ya sea como prestamista o prestatario. Con una comunidad en constante crecimiento, ofrecemos soluciones personalizadas que se adaptan a tus necesidades económicas, ayudándote a alcanzar tus metas financieras de manera eficiente y segura. ¡Forma parte de esta transformación!  
                        </p>
                        <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">
                        Mas información
                        </button>
                    </div>
                    <div className="flex justify-center">
                        <img
                        src={ima4}
                        className="object-cover w-full h-80 rounded-md"
                        />
                    </div>
                </div>
            </div>
            <div class="sectión-cont">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 custom-bg">
      {/* Columna para la imagen (izquierda) */}
      <div className="flex justify-center">
        <img
          src="https://via.placeholder.com/600"
          alt="Imagen grande"
          className="object-cover w-full h-80 rounded-md"
        />
      </div>

      {/* Columna para el contenido (derecha) */}
      <div className="flex flex-col justify-center">
        <h2 className="text-2xl font-bold mb-4 custom-text-color">
          Nuestros clientes
        </h2>
        <h2 className="text-2xl font-bold mb-4 custom-text-color">
          Tim Smith
        </h2>
        <p className="text-gray-700 mb-4 custom-text-color">
        “La plataforma me permitió diversificar mis inversiones fácilmente y con total transparencia. El proceso de préstamo fue rápido y sin complicaciones.” 
        </p>
        <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">
        Mas información
        </button>
      </div>
    </div>
            </div>
        </section>
        
    );
  }