import { useAuth } from '../hooks/useAuth';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Output } from '../components/Output';

export function Profile() {
  const { user } = useAuth();
  if (!user) return null;

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <Text variant="h1">Mój profil</Text>
      <Card>
        <CardHeader><Text variant="h3">Dane użytkownika</Text></CardHeader>
        <CardBody className="space-y-4">
          <Output label="ID" value={user.id} />
          <Output label="Nazwa użytkownika" value={user.username} />
          <Output label="Email" value={user.email} />
          <Output label="Rola" value={user.role === 'admin' ? 'Administrator' : 'Użytkownik'} />
          <Output label="Status" value={user.is_active ? 'Aktywny' : 'Nieaktywny'} />
        </CardBody>
      </Card>
    </div>
  );
}
