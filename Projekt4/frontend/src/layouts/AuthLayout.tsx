import { Outlet } from 'react-router-dom';
import { Center } from '../components/Center';
import { Card, CardBody } from '../components/Card';
import { Text } from '../components/Text';

export function AuthLayout() {
  return (
    <Center>
      <div className="w-full max-w-sm px-4">
        <div className="mb-8 text-center">
          <Text variant="h1">Zapisy na Fitness</Text>
          <Text variant="body" className="mt-1">
            Zaloguj się lub załóż konto
          </Text>
        </div>
        <Card>
          <CardBody>
            <Outlet />
          </CardBody>
        </Card>
      </div>
    </Center>
  );
}
