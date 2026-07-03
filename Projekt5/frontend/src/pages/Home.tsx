import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Card, CardBody } from '../components/Card';
import { Text } from '../components/Text';
import { Button } from '../components/Button';

export function Home() {
  const { isAuthenticated, isAdmin } = useAuth();

  return (
    <div className="space-y-8">
      <div className="text-center">
        <Text variant="h1">Zarządzanie Pracownikami</Text>
        <Text variant="body" className="mt-2 max-w-2xl mx-auto">
          Twórz grafik pracowników, zarządzaj zmianami, przeglądaj tygodniowe terminarze i rankingi.
        </Text>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Pracownicy</Text>
            <Text variant="body">Przeglądaj listę pracowników i ich grafiki.</Text>
            <Link to="/employees" className="block">
              <Button variant="primary" className="w-full">Zobacz pracowników</Button>
            </Link>
          </CardBody>
        </Card>

        {isAuthenticated && (
          <Card>
            <CardBody className="space-y-3">
              <Text variant="h3">Grafik</Text>
              <Text variant="body">Dodawaj i edytuj zmiany w grafiku pracowników.</Text>
              <Link to="/employees" className="block">
                <Button variant="secondary" className="w-full">Zarządzaj grafikiem</Button>
              </Link>
            </CardBody>
          </Card>
        )}

        {isAdmin && (
          <Card>
            <CardBody className="space-y-3">
              <Text variant="h3">Panel Admin</Text>
              <Text variant="body">Zarządzanie użytkownikami i pracownikami.</Text>
              <Link to="/admin" className="block">
                <Button variant="danger" className="w-full">Panel Admin</Button>
              </Link>
            </CardBody>
          </Card>
        )}
      </div>
    </div>
  );
}
