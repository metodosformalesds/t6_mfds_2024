export const formValidators = {
  first_name: {
    required: "El nombre es requerido",
  },
  middle_name: {

  },
  first_surname: {
    required: "El apellido paterno es requerido",
  },
  second_surname: {
    required: "El apellido materno es requerido",
  },
  birth_date: {
    required: "La fecha de nacimiento es requerida",
    validate: {
      ageLimit: (value) => {
        const birthDate = new Date(value);
        const age = new Date().getFullYear() - birthDate.getFullYear();
        return age >= 18 || "Debes ser mayor de 18 años";
      },
    },
  },
  full_address: {
    required: "La dirección es requerida",
  },
  city: {
    required: "La ciudad es requerida",
  },
  neighborhood: {
    required: "El vecindario es requerido",
  },
  postal_code: {
    required: "El código postal es requerido",
    pattern: {
      value: /^[0-9]{5}$/,
      message: "El código postal debe ser de 5 dígitos",
    },
  },
  state: {
    required: "El estado es requerido",
  },
  country: {
    required: "El país es requerido",
  },
  rfc: {
    required: "El RFC es requerido",
    pattern: {
      value: /^[A-ZÑ&]{3,4}\d{6}(?:[A-Z\d]{3})?$/,
      message: "El RFC no es válido",
    },
  },
  ciec: {
    required: "La CIEC es requerida",
  },
  phone_number: {
    required: "El número de contacto es requerido",
    pattern: {
      value: /^[0-9]{10}$/,  // Ajustar según el tamaño permitido en el modelo
      message: "El número debe ser de 10 dígitos",
    },
  },
  identificationImage: {
    required: "La imagen de identificación es requerida",
  },
  email: {
    required: "El correo electrónico es requerido",
    pattern: {
      value: /^\S+@\S+\.\S+$/,
      message: "El correo electrónico no es válido",
    },
  },
  password: {
    required: "La contraseña es requerida",
    pattern: {
      value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
      message:
        "La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial",
    },
  },
};
