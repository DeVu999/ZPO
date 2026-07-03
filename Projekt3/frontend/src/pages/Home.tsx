import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Card, CardBody } from '../components/Card';
import { Text } from '../components/Text';
import { Button } from '../components/Button';

export function Home() {
  const { isAdmin } = useAuth();

  return (
    <div className="space-y-8">
      <div className="text-center">
        <Text variant="h1">Rezerwacja Salek</Text>
        <Text variant="body" className="mt-2 max-w-2xl mx-auto">
          Przeglądaj dostępne sale, rezerwuj terminy i zarządzaj swoimi
          rezerwacjami. Aplikacja używa React, TypeScript, FastAPI i JWT.
        </Text>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Sale</Text>
            <Text variant="body">
              Przeglądaj dostępne sale i sprawdzaj ich opisy oraz pojemność.
            </Text>
            <Link to="/rooms" className="block">
              <Button variant="primary" className="w-full">
                Zobacz sale
              </Button>
            </Link>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Moje Rezerwacje</Text>
            <Text variant="body">
              Zarządzaj swoimi rezerwacjami sal.
            </Text>
            <Link to="/my-bookings" className="block">
              <Button variant="secondary" className="w-full">
                Moje rezerwacje
              </Button>
            </Link>
          </CardBody>
        </Card>

        {isAdmin && (
        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Panel Admin</Text>
            <Text variant="body">
              Zarządzanie salami, użytkownikami i rezerwacjami.
            </Text>
            <Link to="/admin" className="block">
              <Button variant="danger" className="w-full">
                Panel Admin
              </Button>
            </Link>
          </CardBody>
        </Card>
        )}
      </div>
    </div>
  );
}
