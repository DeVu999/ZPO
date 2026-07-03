import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Form } from '../components/Form';
import { ErrorMessage } from '../components/ErrorMessage';
import { required, minLength } from '../utils/validators';

interface LoginForm {
  username: string;
  password: string;
}

export function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const methods = useForm<LoginForm>({
    defaultValues: { username: '', password: '' },
  });

  const onSubmit = async (data: LoginForm) => {
    setIsLoading(true);
    setError(null);
    try {
      await login(data);
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd logowania');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <ErrorMessage message={error} />

      <Form methods={methods} onSubmit={onSubmit}>
        <Input
          name="username"
          label="Nazwa użytkownika"
          placeholder="Wpisz nazwę użytkownika"
          rules={{ validate: { required } }}
        />

        <Input
          name="password"
          type="password"
          label="Hasło"
          placeholder="Wpisz hasło"
          rules={{ validate: { required, minLength: minLength(3) } }}
        />

        <Button type="submit" isLoading={isLoading} className="w-full">
          Zaloguj się
        </Button>
      </Form>

      <p className="text-center text-sm text-gray-500">
        Nie masz konta?{' '}
        <Link to="/register" className="font-medium text-blue-600 hover:text-blue-500">
          Zarejestruj się
        </Link>
      </p>
    </div>
  );
}
