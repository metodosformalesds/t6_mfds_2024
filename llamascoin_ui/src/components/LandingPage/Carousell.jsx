import { Carousel } from "@material-tailwind/react";
import imagen1 from '../../assets/Images_Carrusel/1.jpg'
import imagen2 from '../../assets/Images_Carrusel/2.jpg'
import imagen3 from '../../assets/Images_Carrusel/3.jpg'
export function CarouselDefault() {
  return (
    <Carousel className="rounded-xl">
      <img
        src={imagen1}
        alt="image 1"
        className="h-full w-full max-h-[460px] object-cover"
      />
      <img
        src={imagen2}
        alt="image 2"
        className="h-full w-full max-h-[460px] object-cover"
      />
      <img
        src={imagen3}
        alt="image 3"
        className="h-full w-full max-h-[460px] object-cover"
      />
    </Carousel>
  );
}
 