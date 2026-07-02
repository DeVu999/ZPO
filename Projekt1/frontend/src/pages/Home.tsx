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
        <Text variant="h1">Witaj w Projekcie 1</Text>
        <Text variant="body" className="mt-2 max-w-2xl mx-auto">
          Aplikacja demonstrująca pełny stos technologiczny:
          React, TypeScript, Tailwind CSS, FastAPI, JWT, WebSocket.
        </Text>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Strefa użytkownika</Text>
            <Text variant="body">
              Przeglądaj i zarządzaj swoimi zasobami po zalogowaniu.
            </Text>
            {!isAuthenticated && (
              <Link to="/login" className="block">
                <Button variant="primary" className="w-full">
                  Zaloguj się
                </Button>
              </Link>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">Panel administracyjny</Text>
            <Text variant="body">
              Zarządzanie użytkownikami i konfiguracją systemu.
            </Text>
            {isAdmin && (
              <Link to="/admin" className="block">
                <Button variant="danger" className="w-full">
                  Panel Admin
                </Button>
              </Link>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardBody className="space-y-3">
            <Text variant="h3">WebSocket</Text>
            <Text variant="body">
              Komunikacja w czasie rzeczywistym za pomocą WebSocket.
            </Text>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
