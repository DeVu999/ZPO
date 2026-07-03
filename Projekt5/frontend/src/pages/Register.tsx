import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Form } from '../components/Form';
import { ErrorMessage } from '../components/ErrorMessage';
import { required, minLength, email, passwordStrength } from '../utils/validators';

interface RegisterForm {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export function Register() {
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const methods = useForm<RegisterForm>({
    defaultValues: { username: '', email: '', password: '', confirmPassword: '' },
  });

  const onSubmit = async (data: RegisterForm) => {
    if (data.password !== data.confirmPassword) {
      setError('Hasła nie są zgodne');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      await registerUser({ username: data.username, email: data.email, password: data.password });
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd rejestracji');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <ErrorMessage message={error} />
      <Form methods={methods} onSubmit={onSubmit}>
        <Input name="username" label="Nazwa użytkownika" placeholder="Wpisz nazwę użytkownika" rules={{ validate: { required, minLength: minLength(3) } }} />
        <Input name="email" type="email" label="Email" placeholder="Wpisz adres email" rules={{ validate: { required, email } }} />
        <Input name="password" type="password" label="Hasło" placeholder="Wpisz hasło" rules={{ validate: { required, passwordStrength } }} />
        <Input name="confirmPassword" type="password" label="Potwierdź hasło" placeholder="Powtórz hasło" rules={{ validate: { required } }} />
        <Button type="submit" isLoading={isLoading} className="w-full">Zarejestruj się</Button>
      </Form>
      <p className="text-center text-sm text-gray-500">
        Masz już konto?{' '}
        <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500">Zaloguj się</Link>
      </p>
    </div>
  );
}
