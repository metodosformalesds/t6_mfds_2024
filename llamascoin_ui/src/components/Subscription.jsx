import { CheckIcon } from "@heroicons/react/24/solid";
const Tier = {
  name: "Plan Prestamista",
  id: "tier-enterprise",
  href: "/register",
  priceMonthly: "$50",
  description: "Accede a los beneficios de prestar dinero.",
  features: [
    "Publica hasta 5 prestamos",
    "Accede a informacion de los prestatarios",
    "Eligue a quien prestar",
    "Notificaciones",
    "Dashboard con tus ganancias",
  ],
  featured: true,
};

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

export default function Subscription() {
  return (
    <div className="w-100 items-center gap-y-6 lg:max-xl">
      <div
        className={classNames(
          "relative bg-gray-900 shadow-2xl",
          "rounded-3xl p-8 ring-1 ring-gray-900/10 sm:p-10"
        )}
      >
        <h3
          id={Tier.id}
          className={classNames(
            "text-indigo-400",
            "text-base font-semibold leading-7"
          )}
        >
          {Tier.name}
        </h3>
        <p className="mt-4 flex items-baseline gap-x-2">
          <span className="text-white text-5xl font-bold tracking-tight">
            {Tier.priceMonthly}
          </span>
          <span className="text-gray-400 text-base">/mes</span>
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
      </div>
    </div>
  );
}
