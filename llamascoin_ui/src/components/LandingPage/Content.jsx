import '../LandingPage/css.css';
import Stripe from '../../assets/landingpage/stripe.png'
import Buro from '../../assets/landingpage/buro.png'
import {Card,CardHeader,CardBody,CardFooter,Typography,Button,} from "@material-tailwind/react";
export function ContentDesign() {
    return(
        <section class="content1">
            <div class="sección-cont">
                <h2 class="heading-t"> Nuestros  <span>Clientes</span></h2>
                <h2 class="subtext">Nuestros socios</h2>
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
                                src="https://images.unsplash.com/photo-1540553016722-983e48a2cd10?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80"
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
                            src="https://images.unsplash.com/photo-1540553016722-983e48a2cd10?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80"
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
                            src="https://images.unsplash.com/photo-1540553016722-983e48a2cd10?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80"
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
                
            </div>
        </section>
        
    );
  }