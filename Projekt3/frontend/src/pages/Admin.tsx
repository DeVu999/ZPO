import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useFetch } from '../hooks/useFetch';
import { roomService } from '../services/roomService';
import { userService } from '../services/userService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Table } from '../components/Table';
import { Button } from '../components/Button';
import { ErrorMessage } from '../components/ErrorMessage';
import { PageLoading } from '../components/Loading';
import { Modal } from '../components/Modal';
import { Input } from '../components/Input';
import { Form } from '../components/Form';
import { Output } from '../components/Output';
import { useForm } from 'react-hook-form';
import { required, positiveNumber } from '../utils/validators';
import type { Room } from '../types/Room';
import type { User } from '../types/User';

interface RoomFormData {
  name: string;
  capacity: string;
  description: string;
}

export function Admin() {
  const { user: currentUser } = useAuth();
  const [activeTab, setActiveTab] = useState<'rooms' | 'users'>('rooms');

  const {
    data: rooms,
    isLoading: roomsLoading,
    error: roomsError,
    refetch: refetchRooms,
  } = useFetch((_signal) => roomService.getAll(), []);

  const {
    data: users,
    isLoading: usersLoading,
    error: usersError,
    refetch: refetchUsers,
  } = useFetch((_signal) => userService.getAll(), []);

  const [editRoom, setEditRoom] = useState<Room | null>(null);
  const [isAddRoom, setIsAddRoom] = useState(false);
  const [roomActionLoading, setRoomActionLoading] = useState(false);
  const [roomActionError, setRoomActionError] = useState<string | null>(null);
  const [deleteRoomTarget, setDeleteRoomTarget] = useState<Room | null>(null);

  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [userActionLoading, setUserActionLoading] = useState(false);
  const [userActionError, setUserActionError] = useState<string | null>(null);

  const roomMethods = useForm<RoomFormData>({
    defaultValues: { name: '', capacity: '', description: '' },
  });

  const openAddRoom = () => {
    roomMethods.reset({ name: '', capacity: '', description: '' });
    setEditRoom(null);
    setIsAddRoom(true);
    setRoomActionError(null);
  };

  const openEditRoom = (room: Room) => {
    roomMethods.reset({
      name: room.name,
      capacity: String(room.capacity),
      description: room.description,
    });
    setEditRoom(room);
    setIsAddRoom(true);
    setRoomActionError(null);
  };

  const handleSaveRoom = async (data: RoomFormData) => {
    setRoomActionLoading(true);
    setRoomActionError(null);
    try {
      const payload = {
        name: data.name,
        capacity: parseInt(data.capacity),
        description: data.description,
      };
      if (editRoom) {
        await roomService.update(editRoom.id, payload);
      } else {
        await roomService.create(payload);
      }
      setIsAddRoom(false);
      setEditRoom(null);
      refetchRooms();
    } catch (err) {
      setRoomActionError(err instanceof Error ? err.message : 'Błąd');
    } finally {
      setRoomActionLoading(false);
    }
  };

  const handleDeleteRoom = async () => {
    if (!deleteRoomTarget) return;
    setRoomActionLoading(true);
    setRoomActionError(null);
    try {
      await roomService.delete(deleteRoomTarget.id);
      setDeleteRoomTarget(null);
      refetchRooms();
    } catch (err) {
      setRoomActionError(err instanceof Error ? err.message : 'Błąd');
    } finally {
      setRoomActionLoading(false);
    }
  };

  const handleToggleActive = async (targetUser: User) => {
    if (targetUser.id === currentUser?.id) return;
    setUserActionLoading(true);
    setUserActionError(null);
    try {
      await userService.toggleActive(targetUser.id);
      setSelectedUser(null);
      refetchUsers();
    } catch (err) {
      setUserActionError(err instanceof Error ? err.message : 'Błąd');
    } finally {
      setUserActionLoading(false);
    }
  };

  const roomColumns = [
    { key: 'id', header: 'ID' },
    { key: 'name', header: 'Nazwa' },
    { key: 'capacity', header: 'Pojemność' },
    {
      key: 'description',
      header: 'Opis',
      render: (item: Room) => (
        <span className="max-w-xs truncate block">
          {item.description || '-'}
        </span>
      ),
    },
    {
      key: 'actions',
      header: 'Akcje',
      render: (item: Room) => (
        <div className="flex gap-2">
          <Button
            variant="secondary"
            onClick={(e) => {
              e.stopPropagation();
              openEditRoom(item);
            }}
          >
            Edytuj
          </Button>
          <Button
            variant="danger"
            onClick={(e) => {
              e.stopPropagation();
              setDeleteRoomTarget(item);
            }}
          >
            Usuń
          </Button>
        </div>
      ),
    },
  ];

  const userColumns = [
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
          <Text variant="body">Zarządzanie salami i użytkownikami.</Text>
        </div>
        <div className="flex gap-2">
          <Button
            variant={activeTab === 'rooms' ? 'primary' : 'secondary'}
            onClick={() => setActiveTab('rooms')}
          >
            Sale
          </Button>
          <Button
            variant={activeTab === 'users' ? 'primary' : 'secondary'}
            onClick={() => setActiveTab('users')}
          >
            Użytkownicy
          </Button>
        </div>
      </div>

      {activeTab === 'rooms' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <Text variant="h2">Sale</Text>
            <div className="flex gap-2">
              <Button variant="primary" onClick={openAddRoom}>
                Dodaj salę
              </Button>
              <Button variant="secondary" onClick={refetchRooms}>
                Odśwież
              </Button>
            </div>
          </div>

          <Card>
            <CardHeader>
              <Text variant="h3">Lista sal</Text>
            </CardHeader>
            <CardBody>
              <ErrorMessage message={roomsError} onRetry={refetchRooms} />
              {roomsLoading ? (
                <PageLoading />
              ) : (
                <Table
                  columns={roomColumns}
                  data={rooms ?? []}
                  emptyMessage="Brak sal"
                />
              )}
            </CardBody>
          </Card>
        </div>
      )}

      {activeTab === 'users' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <Text variant="h2">Użytkownicy</Text>
            <Button variant="secondary" onClick={refetchUsers}>
              Odśwież
            </Button>
          </div>

          <Card>
            <CardHeader>
              <Text variant="h3">Lista użytkowników</Text>
            </CardHeader>
            <CardBody>
              <ErrorMessage message={usersError} onRetry={refetchUsers} />
              {usersLoading ? (
                <PageLoading />
              ) : (
                <Table
                  columns={userColumns}
                  data={users ?? []}
                  onRowClick={(user) => setSelectedUser(user)}
                />
              )}
            </CardBody>
          </Card>
        </div>
      )}

      <Modal
        isOpen={isAddRoom}
        onClose={() => {
          setIsAddRoom(false);
          setEditRoom(null);
          setRoomActionError(null);
        }}
        title={editRoom ? 'Edytuj salę' : 'Dodaj salę'}
      >
        <div className="space-y-4">
          <ErrorMessage message={roomActionError} />

          <Form methods={roomMethods} onSubmit={handleSaveRoom}>
            <Input
              name="name"
              label="Nazwa sali"
              placeholder="Np. Sala A"
              rules={{ validate: { required } }}
            />

            <Input
              name="capacity"
              label="Pojemność"
              type="number"
              placeholder="Np. 30"
              rules={{ validate: { required, positiveNumber } }}
            />

            <Input
              name="description"
              label="Opis"
              placeholder="Opis sali..."
            />

            <div className="flex gap-3 pt-2">
              <Button
                type="submit"
                variant="primary"
                isLoading={roomActionLoading}
              >
                {editRoom ? 'Zapisz' : 'Dodaj'}
              </Button>
              <Button
                variant="ghost"
                onClick={() => {
                  setIsAddRoom(false);
                  setEditRoom(null);
                }}
              >
                Anuluj
              </Button>
            </div>
          </Form>
        </div>
      </Modal>

      <Modal
        isOpen={!!deleteRoomTarget}
        onClose={() => {
          setDeleteRoomTarget(null);
          setRoomActionError(null);
        }}
        title="Usuń salę"
      >
        <div className="space-y-4">
          <Text variant="body">
            Czy na pewno chcesz usunąć salę "{deleteRoomTarget?.name}"?
          </Text>

          <ErrorMessage message={roomActionError} />

          <div className="flex gap-3 pt-2">
            <Button
              variant="danger"
              isLoading={roomActionLoading}
              onClick={handleDeleteRoom}
            >
              Usuń
            </Button>
            <Button
              variant="ghost"
              onClick={() => setDeleteRoomTarget(null)}
            >
              Anuluj
            </Button>
          </div>
        </div>
      </Modal>

      <Modal
        isOpen={!!selectedUser}
        onClose={() => {
          setSelectedUser(null);
          setUserActionError(null);
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

            <ErrorMessage message={userActionError} />

            <div className="flex gap-3 pt-2">
              <Button
                variant={selectedUser.is_active ? 'secondary' : 'primary'}
                isLoading={userActionLoading}
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
