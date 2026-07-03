import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '../hooks/useAuth';
import { useFetch } from '../hooks/useFetch';
import { classService } from '../services/classService';
import { userService } from '../services/userService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Table } from '../components/Table';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Form } from '../components/Form';
import { ErrorMessage } from '../components/ErrorMessage';
import { PageLoading } from '../components/Loading';
import { Modal } from '../components/Modal';
import { Output } from '../components/Output';
import { formatDateTime } from '../utils/helpers';
import { required } from '../utils/validators';
import type { User } from '../types/User';
import type { FitnessClass } from '../types/Fitness';

interface ClassFormData {
  name: string;
  description: string;
  instructor: string;
  datetime: string;
  capacity: string;
}

export function Admin() {
  const { user: currentUser } = useAuth();

  const {
    data: classes,
    isLoading: classesLoading,
    error: classesError,
    refetch: refetchClasses,
  } = useFetch((_signal) => classService.getAll(), []);

  const {
    data: users,
    isLoading: usersLoading,
    error: usersError,
    refetch: refetchUsers,
  } = useFetch((_signal) => userService.getAll(), []);

  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [editingClass, setEditingClass] = useState<FitnessClass | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  const classMethods = useForm<ClassFormData>({
    defaultValues: {
      name: '',
      description: '',
      instructor: '',
      datetime: '',
      capacity: '20',
    },
  });

  const handleCreateClass = async (data: ClassFormData) => {
    setActionLoading(true);
    setActionError(null);
    try {
      await classService.create({
        name: data.name,
        description: data.description,
        instructor: data.instructor,
        datetime: new Date(data.datetime).toISOString(),
        capacity: Number(data.capacity),
      });
      setShowCreateModal(false);
      classMethods.reset();
      refetchClasses();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Błąd tworzenia');
    } finally {
      setActionLoading(false);
    }
  };

  const handleUpdateClass = async (data: ClassFormData) => {
    if (!editingClass) return;
    setActionLoading(true);
    setActionError(null);
    try {
      await classService.update(editingClass.id, {
        name: data.name,
        description: data.description,
        instructor: data.instructor,
        datetime: new Date(data.datetime).toISOString(),
        capacity: Number(data.capacity),
      });
      setEditingClass(null);
      classMethods.reset();
      refetchClasses();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Błąd aktualizacji');
    } finally {
      setActionLoading(false);
    }
  };

  const handleDeleteClass = async (id: number) => {
    setActionLoading(true);
    setActionError(null);
    try {
      await classService.delete(id);
      setEditingClass(null);
      refetchClasses();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Błąd usuwania');
    } finally {
      setActionLoading(false);
    }
  };

  const openEditModal = (item: FitnessClass) => {
    setEditingClass(item);
    classMethods.reset({
      name: item.name,
      description: item.description,
      instructor: item.instructor,
      datetime: item.datetime.slice(0, 16),
      capacity: String(item.capacity),
    });
  };

  const openCreateModal = () => {
    setShowCreateModal(true);
    classMethods.reset({
      name: '',
      description: '',
      instructor: '',
      datetime: '',
      capacity: '20',
    });
  };

  const handleToggleActive = async (targetUser: User) => {
    if (targetUser.id === currentUser?.id) return;
    setActionLoading(true);
    setActionError(null);
    try {
      await userService.toggleActive(targetUser.id);
      setSelectedUser(null);
      refetchUsers();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Błąd');
    } finally {
      setActionLoading(false);
    }
  };

  const classColumns = [
    { key: 'id', header: 'ID' },
    { key: 'name', header: 'Nazwa' },
    { key: 'instructor', header: 'Prowadzący' },
    {
      key: 'datetime',
      header: 'Data',
      render: (item: FitnessClass) => formatDateTime(item.datetime),
    },
    {
      key: 'spots',
      header: 'Miejsca',
      render: (item: FitnessClass) => `${item.capacity - item.free_spots}/${item.capacity}`,
    },
    {
      key: 'actions',
      header: 'Akcje',
      render: (item: FitnessClass) => (
        <div className="flex gap-2">
          <Button variant="secondary" onClick={(e) => { e.stopPropagation(); openEditModal(item); }}>
            Edytuj
          </Button>
          <Button variant="danger" onClick={(e) => { e.stopPropagation(); handleDeleteClass(item.id); }}>
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
          <Text variant="body">Zarządzanie zajęciami i użytkownikami.</Text>
        </div>
      </div>

      <ErrorMessage message={classesError ?? usersError ?? actionError} />

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <Text variant="h3">Zajęcia</Text>
            <Button variant="primary" onClick={openCreateModal}>
              Dodaj zajęcia
            </Button>
          </div>
        </CardHeader>
        <CardBody>
          {classesLoading ? (
            <PageLoading />
          ) : (
            <Table columns={classColumns} data={classes ?? []} />
          )}
        </CardBody>
      </Card>

      <Card>
        <CardHeader>
          <Text variant="h3">Użytkownicy</Text>
        </CardHeader>
        <CardBody>
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

      <Modal
        isOpen={!!editingClass}
        onClose={() => { setEditingClass(null); setActionError(null); }}
        title="Edytuj zajęcia"
      >
        {editingClass && (
          <Form methods={classMethods} onSubmit={handleUpdateClass}>
            <Input name="name" label="Nazwa" rules={{ validate: { required } }} />
            <Input name="description" label="Opis" />
            <Input name="instructor" label="Prowadzący" rules={{ validate: { required } }} />
            <Input name="datetime" label="Data" type="datetime-local" rules={{ validate: { required } }} />
            <Input name="capacity" label="Miejsca" type="number" rules={{ validate: { required } }} />
            <div className="flex gap-3 pt-2">
              <Button type="submit" isLoading={actionLoading}>Zapisz</Button>
              <Button variant="ghost" onClick={() => setEditingClass(null)}>Anuluj</Button>
            </div>
          </Form>
        )}
      </Modal>

      <Modal
        isOpen={showCreateModal}
        onClose={() => { setShowCreateModal(false); setActionError(null); }}
        title="Dodaj zajęcia"
      >
        <Form methods={classMethods} onSubmit={handleCreateClass}>
          <Input name="name" label="Nazwa" rules={{ validate: { required } }} />
          <Input name="description" label="Opis" />
          <Input name="instructor" label="Prowadzący" rules={{ validate: { required } }} />
          <Input name="datetime" label="Data" type="datetime-local" rules={{ validate: { required } }} />
          <Input name="capacity" label="Miejsca" type="number" rules={{ validate: { required } }} />
          <div className="flex gap-3 pt-2">
            <Button type="submit" isLoading={actionLoading}>Dodaj</Button>
            <Button variant="ghost" onClick={() => setShowCreateModal(false)}>Anuluj</Button>
          </div>
        </Form>
      </Modal>

      <Modal
        isOpen={!!selectedUser}
        onClose={() => { setSelectedUser(null); setActionError(null); }}
        title="Szczegóły użytkownika"
      >
        {selectedUser && (
          <div className="space-y-4">
            <Output label="ID" value={selectedUser.id} />
            <Output label="Nazwa użytkownika" value={selectedUser.username} />
            <Output label="Email" value={selectedUser.email} />
            <Output label="Rola" value={selectedUser.role === 'admin' ? 'Administrator' : 'Użytkownik'} />
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
