import { useState } from 'react';
import { useFetch } from '../hooks/useFetch';
import { employeeService } from '../services/employeeService';
import { userService } from '../services/userService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Table } from '../components/Table';
import { Button } from '../components/Button';
import { PageLoading } from '../components/Loading';
import { Modal } from '../components/Modal';
import { Input } from '../components/Input';
import { Form } from '../components/Form';
import { useForm } from 'react-hook-form';
import { required } from '../utils/validators';
import type { Employee } from '../types/Employee';

interface EmployeeFormData {
  name: string;
  position: string;
  department: string;
}

export function Admin() {
  const { data: users, isLoading: usersLoading } = useFetch(() => userService.getAll(), []);
  const { data: employees, isLoading: empLoading, refetch: refetchEmp } = useFetch(() => employeeService.getAll(), []);
  const [tab, setTab] = useState<'users' | 'employees'>('employees');
  const [showAddEmp, setShowAddEmp] = useState(false);

  const methods = useForm<EmployeeFormData>({
    defaultValues: { name: '', position: '', department: '' },
  });

  const handleAddEmployee = async (data: EmployeeFormData) => {
    try {
      await employeeService.create(data);
      setShowAddEmp(false);
      methods.reset();
      refetchEmp();
    } catch { /* ignore */ }
  };

  const handleDeleteEmployee = async (id: number) => {
    try {
      await employeeService.delete(id);
      refetchEmp();
    } catch { /* ignore */ }
  };

  const userColumns = [
    { key: 'id', header: 'ID' },
    { key: 'username', header: 'Nazwa' },
    { key: 'email', header: 'Email' },
    { key: 'role', header: 'Rola' },
  ];

  const empColumns = [
    { key: 'id', header: 'ID' },
    { key: 'name', header: 'Imię i nazwisko' },
    { key: 'position', header: 'Stanowisko' },
    { key: 'department', header: 'Dział' },
    {
      key: 'actions',
      header: '',
      render: (item: Employee) => (
        <Button variant="danger" onClick={(e) => { e.stopPropagation(); handleDeleteEmployee(item.id); }}>Usuń</Button>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <Text variant="h1">Panel administracyjny</Text>

      <div className="flex gap-2 border-b border-gray-200 pb-2">
        <Button variant={tab === 'employees' ? 'primary' : 'ghost'} onClick={() => setTab('employees')}>Pracownicy</Button>
        <Button variant={tab === 'users' ? 'primary' : 'ghost'} onClick={() => setTab('users')}>Użytkownicy</Button>
      </div>

      {tab === 'employees' && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <Text variant="h3">Pracownicy</Text>
              <Button variant="primary" onClick={() => setShowAddEmp(true)}>Dodaj pracownika</Button>
            </div>
          </CardHeader>
          <CardBody>
            {empLoading ? <PageLoading /> : <Table columns={empColumns} data={employees ?? []} />}
          </CardBody>
        </Card>
      )}

      {tab === 'users' && (
        <Card>
          <CardHeader><Text variant="h3">Użytkownicy</Text></CardHeader>
          <CardBody>
            {usersLoading ? <PageLoading /> : <Table columns={userColumns} data={users ?? []} />}
          </CardBody>
        </Card>
      )}

      <Modal isOpen={showAddEmp} onClose={() => setShowAddEmp(false)} title="Dodaj pracownika">
        <Form methods={methods} onSubmit={handleAddEmployee}>
          <Input name="name" label="Imię i nazwisko" rules={{ validate: { required } }} />
          <Input name="position" label="Stanowisko" rules={{ validate: { required } }} />
          <Input name="department" label="Dział" />
          <Button type="submit" className="w-full">Dodaj</Button>
        </Form>
      </Modal>
    </div>
  );
}
