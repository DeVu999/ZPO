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
        <Text variant="h1">Zapisy na Fitness</Text>
        <Text variant="body" className="mt-2 max-w-2xl mx-auto">
          Przeglądaj dostępne zajęcia fitness, zapisuj się i zarządzaj swoimi
          treningami. Aplikacja używa React, TypeScript, FastAPI, JWT i WebSocket.
        </Text>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Zajęcia</Text>
            <Text variant="body">
              Przeglądaj dostępne zajęcia fitness i zapisz się na wybrane.
            </Text>
            <Link to="/classes" className="block">
              <Button variant="primary" className="w-full">
                Zobacz zajęcia
              </Button>
            </Link>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Moje Zajęcia</Text>
            <Text variant="body">
              Zarządzaj swoimi zapisami i sprawdzaj status zajęć.
            </Text>
            <Link to="/my-classes" className="block">
              <Button variant="secondary" className="w-full">
                Moje zapisy
              </Button>
            </Link>
          </CardBody>
        </Card>

        {isAdmin && (
        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Panel Admin</Text>
            <Text variant="body">
              Zarządzanie zajęciami i użytkownikami systemu.
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
