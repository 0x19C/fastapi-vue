export const isValidEmail = (email: string | null | undefined): boolean => {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return !!email && emailRegex.test(email);
};

export const isStrongPassword = (
  password: string | null | undefined
): boolean => {
  // const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/;
  const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
  return !!password && strongPasswordRegex.test(password);
};
