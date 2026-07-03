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
        <Text variant="h1">Ocena Filmów</Text>
        <Text variant="body" className="mt-2 max-w-2xl mx-auto">
          Przeglądaj filmy, oceniaj je w skali 1-5 i odkrywaj top produkcje
          według gatunku. Aplikacja używa React, TypeScript, FastAPI, JWT i WebSocket.
        </Text>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Lista filmów</Text>
            <Text variant="body">
              Przeglądaj dostępne filmy i sprawdzaj ich średnie oceny.
            </Text>
            <Link to="/movies" className="block">
              <Button variant="primary" className="w-full">
                Zobacz filmy
              </Button>
            </Link>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Top filmy</Text>
            <Text variant="body">
              Najlepiej oceniane filmy według gatunku lub ogólnie.
            </Text>
            <Link to="/top" className="block">
              <Button variant="secondary" className="w-full">
                Ranking
              </Button>
            </Link>
          </CardBody>
        </Card>

        {isAdmin && (
        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Panel Admin</Text>
            <Text variant="body">
              Zarządzanie użytkownikami i konfiguracją systemu.
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
