import { Typography } from "@material-tailwind/react";
import React, { useState } from 'react';

const LINKS = [
  {
    title: "Compañia",
    items: ["Acerca de nosotros", "Contactanos", "Precios"],
  },
  {
    title: "Soporte",
    items: ["Terminos y condiciones", "Politicas de privacidad"],
  },

];

const currentYear = new Date().getFullYear();

export default function Footer() {
  return (
    <footer className="footer-background relative w-full">
    <div className="mx-auto w-full max-w-7xl px-8">
      <div className="grid grid-cols-1 justify-between gap-4 md:grid-cols-2">
        <Typography variant="h5" className="mb-6 footer-text">
          LlamasCoin
        </Typography>
        <div className="grid grid-cols-3 justify-between gap-4">
          {LINKS.map(({ title, items }) => (
            <ul key={title}>
              <Typography
                variant="small"
                className="mb-3 font-medium opacity-40 footer-text"
              >
                {title}
              </Typography>
              {items.map((link) => (
                <li key={link}>
                  <Typography
                    as="a"
                    href="#"
                    className="py-1.5 font-normal footer-text"
                  >
                    {link}
                  </Typography>
                </li>
              ))}
            </ul>
          ))}
        </div>
      </div>
      <div className="mt-12 flex w-full flex-col items-center justify-center border-t footer-border py-4 md:flex-row md:justify-between">
        <Typography
          variant="small"
          className="mb-4 text-center font-normal footer-text md:mb-0"
        >
          &copy; {currentYear}{" "}
          <a href="http://localhost:5173/" className="footer-link">
            LlamasCoin
          </a>. Todos los derechos reservados
        </Typography>

      </div>
    </div>
  </footer>  
  );
}