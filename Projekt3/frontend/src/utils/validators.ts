export const required = (value: string): string | undefined =>
  value.trim() ? undefined : 'To pole jest wymagane';

export const minLength = (min: number) => (value: string): string | undefined =>
  value.length >= min ? undefined : `Minimalna długość to ${min} znaków`;

export const email = (value: string): string | undefined =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? undefined : 'Nieprawidłowy format email';

export const passwordStrength = (value: string): string | undefined => {
  const errors: string[] = [];
  if (value.length < 8) errors.push('minimum 8 znaków');
  if (!/[A-Z]/.test(value)) errors.push('jedna wielka litera');
  if (!/[0-9]/.test(value)) errors.push('jedna cyfra');
  return errors.length ? 'Hasło musi zawierać: ' + errors.join(', ') : undefined;
};

export const positiveNumber = (value: string): string | undefined => {
  const num = Number(value);
  return !isNaN(num) && num > 0 ? undefined : 'Wartość musi być liczbą dodatnią';
};
