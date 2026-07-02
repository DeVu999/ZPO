export const required = (value: string): string | undefined =>
  value.trim() ? undefined : 'To pole jest wymagane';

export const minLength = (min: number) => (value: string): string | undefined =>
  value.length >= min ? undefined : `Minimalna długość to ${min} znaków`;

export const maxLength = (max: number) => (value: string): string | undefined =>
  value.length <= max ? undefined : `Maksymalna długość to ${max} znaków`;

export const email = (value: string): string | undefined =>
  /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? undefined : 'Nieprawidłowy format email';

export const passwordStrength = (value: string): string | undefined => {
  const errors: string[] = [];
  if (value.length < 8) errors.push('minimum 8 znaków');
  if (!/[A-Z]/.test(value)) errors.push('jedna wielka litera');
  if (!/[0-9]/.test(value)) errors.push('jedna cyfra');
  return errors.length ? 'Hasło musi zawierać: ' + errors.join(', ') : undefined;
};
