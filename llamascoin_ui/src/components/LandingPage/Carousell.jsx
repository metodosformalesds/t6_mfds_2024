import { Carousel } from "@material-tailwind/react";
import imagen1 from '../../assets/Images_Carrusel/1.jpg'
import imagen2 from '../../assets/Images_Carrusel/2.jpg'
export function CarouselDefault() {
  return (
    <Carousel className="rounded-xl">
      <img
        src={imagen1}
        alt="image 1"
        className="h-full w-full max-h-96 object-cover"
      />
      <img
        src={imagen2}
        alt="image 2"
        className="h-full w-full max-h-96 object-cover"
      />
      <img
        src="https://images.unsplash.com/photo-1518623489648-a173ef7824f3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2762&q=80"
        alt="image 3"
        className="h-full w-full max-h-96 object-cover"
      />
    </Carousel>
  );
}
 