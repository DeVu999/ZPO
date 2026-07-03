import { Link } from 'react-router-dom';
import { Center } from '../components/Center';
import { Text } from '../components/Text';
import { Button } from '../components/Button';

export function NotFound() {
  return (
    <Center>
      <div className="text-center">
        <p className="text-6xl font-bold text-gray-300">404</p>
        <Text variant="h1" className="mt-4">
          Strona nie znaleziona
        </Text>
        <Text variant="body" className="mt-2">
          Strona, której szukasz, nie istnieje.
        </Text>
        <Link to="/" className="mt-6 inline-block">
          <Button>Wróć do strony głównej</Button>
        </Link>
      </div>
    </Center>
  );
}
