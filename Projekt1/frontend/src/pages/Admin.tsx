import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useFetch } from '../hooks/useFetch';
import { userService } from '../services/userService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Table } from '../components/Table';
import { Button } from '../components/Button';
import { ErrorMessage } from '../components/ErrorMessage';
import { PageLoading } from '../components/Loading';
import { Modal } from '../components/Modal';
import { Output } from '../components/Output';
import type { User } from '../types/User';

export function Admin() {
  const { user: currentUser } = useAuth();
  const {
    data: users,
    isLoading,
    error,
    refetch,
  } = useFetch((_signal) => userService.getAll(), []);

  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [actionLoading, setActionLoading] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  const handleToggleActive = async (targetUser: User) => {
    if (targetUser.id === currentUser?.id) return;
    setActionLoading(true);
    setActionError(null);
    try {
      await userService.toggleActive(targetUser.id);
      setSelectedUser(null);
      refetch();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Błąd');
    } finally {
      setActionLoading(false);
    }
  };

  const columns = [
    { key: 'id', header: 'ID' },
    { key: 'username', header: 'Nazwa użytkownika' },
    { key: 'email', header: 'Email' },
    {
      key: 'role',
      header: 'Rola',
      render: (user: User) => (
        <span
          className={`rounded px-2 py-0.5 text-xs font-medium ${
            user.role === 'admin'
              ? 'bg-red-100 text-red-700'
              : 'bg-blue-100 text-blue-700'
          }`}
        >
          {user.role === 'admin' ? 'Admin' : 'User'}
        </span>
      ),
    },
    {
      key: 'is_active',
      header: 'Status',
      render: (user: User) => (
        <span
          className={`rounded px-2 py-0.5 text-xs font-medium ${
            user.is_active
              ? 'bg-green-100 text-green-700'
              : 'bg-gray-100 text-gray-500'
          }`}
        >
          {user.is_active ? 'Aktywny' : 'Nieaktywny'}
        </span>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Text variant="h1">Panel administracyjny</Text>
          <Text variant="body">Zarządzanie użytkownikami systemu.</Text>
        </div>
        <Button variant="secondary" onClick={refetch}>
          Odśwież
        </Button>
      </div>

      <Card>
        <CardHeader>
          <Text variant="h3">Użytkownicy</Text>
        </CardHeader>
        <CardBody>
          <ErrorMessage message={error} onRetry={refetch} />
          {isLoading ? (
            <PageLoading />
          ) : (
            <Table
              columns={columns}
              data={users ?? []}
              onRowClick={(user) => setSelectedUser(user)}
            />
          )}
        </CardBody>
      </Card>

      <Modal
        isOpen={!!selectedUser}
        onClose={() => {
          setSelectedUser(null);
          setActionError(null);
        }}
        title="Szczegóły użytkownika"
      >
        {selectedUser && (
          <div className="space-y-4">
            <Output label="ID" value={selectedUser.id} />
            <Output label="Nazwa użytkownika" value={selectedUser.username} />
            <Output label="Email" value={selectedUser.email} />
            <Output label="Rola" value={selectedUser.role} />
            <Output
              label="Status"
              value={selectedUser.is_active ? 'Aktywny' : 'Nieaktywny'}
            />

            <ErrorMessage message={actionError} />

            <div className="flex gap-3 pt-2">
              <Button
                variant={selectedUser.is_active ? 'secondary' : 'primary'}
                isLoading={actionLoading}
                onClick={() => handleToggleActive(selectedUser)}
                disabled={selectedUser.id === currentUser?.id}
              >
                {selectedUser.is_active ? 'Dezaktywuj' : 'Aktywuj'}
              </Button>
              <Button variant="ghost" onClick={() => setSelectedUser(null)}>
                Zamknij
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
