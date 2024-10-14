
import { CheckIcon } from '@heroicons/react/20/solid'
import React from "react";
import Layout from "../components/Layout";

const Tier = {
    name: 'Plan Prestamista',
    id: 'tier-enterprise',
    href: '/register',
    priceMonthly: '$50',
    description: 'Accede a los beneficios de prestar dinero.',
    features: [
      'Publica hasta 5 prestamos',
      'Accede a informacion de los prestatarios',
      'Eligue a quien prestar',
      'Notificaciones',
      'Dashboard con tus ganancias',
    ],
    featured: true,
  }

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

const Subscription = () => {
  return (
    <Layout>
      <div className="relative isolate bg-white px-6 py-24 sm:py-32 lg:px-8">
        <div aria-hidden="true" className="absolute inset-x-0 -top-3 -z-10 transform-gpu overflow-hidden px-36 blur-3xl">
          <div
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
            className="mx-auto aspect-[1155/678] w-[72.1875rem] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30"
          />
        </div>
        <div className="mx-auto max-w-2xl text-center lg:max-w-4xl">
          <p className="mt-2 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            ¿Quieres empezar a PRESTAR dinero?
          </p>
        </div>
        <p className="mx-auto mt-6 max-w-2xl text-center text-lg leading-8 text-gray-600">
          Genera rendimientos prestando dinero a personas que necesitan un pretamo personal.
        </p>
        <div className="mx-auto mt-16 max-w-lg grid grid-cols-1 items-center gap-y-6 sm:mt-20 lg:max-w-4xl">
          <div
            className={classNames(
              'relative bg-gray-900 shadow-2xl',
              'rounded-3xl p-8 ring-1 ring-gray-900/10 sm:p-10'
            )}
          >
            <h3
              id={Tier.id}
              className={classNames('text-indigo-400', 'text-base font-semibold leading-7')}
            >
              {Tier.name}
            </h3>
            <p className="mt-4 flex items-baseline gap-x-2">
              <span className="text-white text-5xl font-bold tracking-tight">
                {Tier.priceMonthly}
              </span>
              <span className="text-gray-400 text-base">/Mxn por mes</span>
            </p>
            <p className="text-gray-300 mt-6 text-base leading-7">
              {Tier.description}
            </p>
            <ul
              role="list"
              className="text-gray-300 mt-8 space-y-3 text-sm leading-6 sm:mt-10"
            >
              {Tier.features.map((feature) => (
                <li key={feature} className="flex gap-x-3">
                  <CheckIcon
                    aria-hidden="true"
                    className="text-indigo-400 h-6 w-5 flex-none"
                  />
                  {feature}
                </li>
              ))}
            </ul>
            <a
              href={Tier.href}
              aria-describedby={Tier.id}
              className="bg-indigo-500 text-white shadow-sm hover:bg-indigo-400 focus-visible:outline-indigo-500 mt-8 block rounded-md px-3.5 py-2.5 text-center text-sm font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 sm:mt-10"
            >
              Empieza a ganar
            </a>
          </div>
        </div>
      </div>
    </Layout>
  );
};


export default Subscription;
