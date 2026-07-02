import { useAuth } from '../hooks/useAuth';
import { useFetch } from '../hooks/useFetch';
import { itemService } from '../services/itemService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Table } from '../components/Table';
import { ErrorMessage } from '../components/ErrorMessage';
import { PageLoading } from '../components/Loading';
import { formatDate } from '../utils/helpers';
import type { Item } from '../types/Item';

export function User() {
  const { user } = useAuth();
  const { data: items, isLoading, error, refetch } = useFetch(
    (_signal) => itemService.getAll(),
    []
  );

  if (!user) return null;

  const columns = [
    { key: 'id', header: 'ID' },
    { key: 'name', header: 'Nazwa' },
    {
      key: 'description',
      header: 'Opis',
      render: (item: Item) => item.description || '-',
    },
    {
      key: 'created_at',
      header: 'Utworzono',
      render: (item: Item) => formatDate(item.created_at),
    },
  ];

  return (
    <div className="space-y-6">
      <Text variant="h1">Strefa użytkownika</Text>
      <Text variant="body">
        Witaj, {user.username}. Poniżej znajdują się Twoje zasoby.
      </Text>

      <Card>
        <CardHeader>
          <Text variant="h3">Lista przedmiotów</Text>
        </CardHeader>
        <CardBody>
          <ErrorMessage message={error} onRetry={refetch} />
          {isLoading ? (
            <PageLoading />
          ) : (
            <Table columns={columns} data={items ?? []} />
          )}
        </CardBody>
      </Card>
    </div>
  );
}
