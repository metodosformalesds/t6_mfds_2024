
export const formValidators = {
    firstName: {
      required: "El nombre es requerido",
    },
    lastName: {
      required: "El apellido paterno es requerido",
    },
    secondLastName: {
      required: "El apellido materno es requerido",
    },
    birthdate: {
      required: "La fecha de nacimiento es requerida",
      validate: {
        ageLimit: (value) => {
          const birthDate = new Date(value);
          const age = new Date().getFullYear() - birthDate.getFullYear();
          return age >= 18 || "Debes ser mayor de 18 años";
        },
      },
    },
    address: {
      required: "La dirección es requerida",
    },
    municipality: {
      required: "El municipio es requerido",
    },
    postalCode: {
      required: "El código postal es requerido",
      pattern: {
        value: /^[0-9]{5}$/,
        message: "El código postal debe ser de 5 dígitos",
      },
    },
    state: {
      required: "El estado es requerido",
    },
    rfc: {
      required: "El RFC es requerido",
      pattern: {
        value: /^[A-ZÑ&]{3,4}\d{6}(?:[A-Z\d]{3})?$/,
        message: "El RFC no es válido",
      },
    },
    number: {
      required: "El número de contacto es requerido",
      pattern: {
        value: /^[0-9]{10}$/,
        message: "El número debe ser de 10 dígitos",
      },
    },
    identificationImage: {
      required: "La imagen de identificación es requerida",
    },
    clabe: {
      required: "La CLABE es requerida",
      pattern: {
        value: /^[0-9]{18}$/,
        message: "La CLABE debe ser de 18 dígitos",
      },
    },
    creditCard: {
      required: "El número de la tarjeta es requerido",
      pattern: {
        value: /^[0-9]{12}$/,
        message: "La tarjeta de crédito debe tener 12 dígitos",
      },
    },
    accountType: {
      required: "El tipo de cuenta es requerido",
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
  