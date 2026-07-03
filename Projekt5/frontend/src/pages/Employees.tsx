import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useFetch } from '../hooks/useFetch';
import { employeeService } from '../services/employeeService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Table } from '../components/Table';
import { Button } from '../components/Button';
import { Modal } from '../components/Modal';
import { Input } from '../components/Input';
import { Form } from '../components/Form';
import { ErrorMessage } from '../components/ErrorMessage';
import { PageLoading } from '../components/Loading';
import { useForm } from 'react-hook-form';
import { required } from '../utils/validators';
import type { Employee, Shift } from '../types/Employee';

interface ShiftFormData {
  shift_date: string;
  start_time: string;
  end_time: string;
  task: string;
}

export function Employees() {
  const { isAuthenticated } = useAuth();
  const { data: employees, isLoading, error, refetch } = useFetch(() => employeeService.getAll(), []);
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [shifts, setShifts] = useState<Shift[]>([]);
  const [showShiftModal, setShowShiftModal] = useState(false);
  const [showAddShift, setShowAddShift] = useState(false);
  const [ranking, setRanking] = useState<{id:number;name:string;position:string;hours:number}[]>([]);
  const [showRanking, setShowRanking] = useState(false);

  const methods = useForm<ShiftFormData>({
    defaultValues: { shift_date: '', start_time: '', end_time: '', task: '' },
  });

  const handleSelectEmployee = async (emp: Employee) => {
    setSelectedEmployee(emp);
    try {
      const s = await employeeService.getShifts(emp.id);
      setShifts(s);
      setShowShiftModal(true);
    } catch { /* ignore */ }
  };

  const handleAddShift = async (data: ShiftFormData) => {
    if (!selectedEmployee) return;
    try {
      await employeeService.createShift({
        employee_id: selectedEmployee.id,
        shift_date: data.shift_date,
        start_time: data.start_time,
        end_time: data.end_time,
        task: data.task,
      });
      setShowAddShift(false);
      const s = await employeeService.getShifts(selectedEmployee.id);
      setShifts(s);
      refetch();
    } catch { /* ignore */ }
  };

  const handleDeleteShift = async (shiftId: number) => {
    try {
      await employeeService.deleteShift(shiftId);
      if (selectedEmployee) {
        const s = await employeeService.getShifts(selectedEmployee.id);
        setShifts(s);
      }
    } catch { /* ignore */ }
  };

  const handleShowRanking = async () => {
    try {
      const now = new Date();
      const start = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split('T')[0];
      const end = now.toISOString().split('T')[0];
      const r = await employeeService.getRanking(start, end, 10);
      setRanking(r);
      setShowRanking(true);
    } catch { /* ignore */ }
  };

  const columns = [
    { key: 'id', header: 'ID' },
    { key: 'name', header: 'Imię i nazwisko' },
    { key: 'position', header: 'Stanowisko' },
    {
      key: 'department',
      header: 'Dział',
      render: (item: Employee) => item.department || '-',
    },
    {
      key: 'actions',
      header: 'Akcje',
      render: (item: Employee) => (
        <div className="flex gap-2">
          <Button variant="secondary" onClick={(e) => { e.stopPropagation(); handleSelectEmployee(item); }}>
            Grafik
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Text variant="h1">Pracownicy</Text>
          <Text variant="body">Zarządzanie pracownikami i grafikiem.</Text>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={handleShowRanking}>Ranking</Button>
          <Button variant="secondary" onClick={refetch}>Odśwież</Button>
        </div>
      </div>

      <Card>
        <CardHeader><Text variant="h3">Lista pracowników</Text></CardHeader>
        <CardBody>
          <ErrorMessage message={error} onRetry={refetch} />
          {isLoading ? <PageLoading /> : <Table columns={columns} data={employees ?? []} onRowClick={handleSelectEmployee} />}
        </CardBody>
      </Card>

      <Modal isOpen={showShiftModal} onClose={() => { setShowShiftModal(false); setSelectedEmployee(null); }} title={`Grafik: ${selectedEmployee?.name}`}>
        {selectedEmployee && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div><span className="font-medium">Stanowisko:</span> {selectedEmployee.position}</div>
              <div><span className="font-medium">Dział:</span> {selectedEmployee.department || '-'}</div>
            </div>
            {isAuthenticated && (
              <Button variant="primary" className="w-full" onClick={() => setShowAddShift(true)}>Dodaj zmianę</Button>
            )}
            {shifts.length === 0 ? (
              <p className="text-sm text-gray-500 text-center py-4">Brak zmian w grafiku</p>
            ) : (
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {shifts.map((s) => (
                  <div key={s.id} className="flex items-center justify-between rounded border border-gray-200 p-3 text-sm">
                    <div>
                      <p className="font-medium">{s.shift_date}</p>
                      <p className="text-gray-500">{s.start_time} - {s.end_time} | {s.task || 'Bez zadania'}</p>
                    </div>
                    {isAuthenticated && (
                      <Button variant="ghost" onClick={() => handleDeleteShift(s.id)}>Usuń</Button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </Modal>

      <Modal isOpen={showAddShift} onClose={() => setShowAddShift(false)} title="Dodaj zmianę">
        <Form methods={methods} onSubmit={handleAddShift}>
          <Input name="shift_date" type="date" label="Data" rules={{ validate: { required } }} />
          <Input name="start_time" type="time" label="Godzina rozpoczęcia" rules={{ validate: { required } }} />
          <Input name="end_time" type="time" label="Godzina zakończenia" rules={{ validate: { required } }} />
          <Input name="task" label="Zadanie" placeholder="Opis zadania" />
          <Button type="submit" className="w-full">Dodaj</Button>
        </Form>
      </Modal>

      <Modal isOpen={showRanking} onClose={() => setShowRanking(false)} title="Ranking pracowników (bieżący miesiąc)">
        {ranking.length === 0 ? (
          <p className="text-sm text-gray-500 text-center py-4">Brak danych</p>
        ) : (
          <div className="space-y-2">
            {ranking.map((r, i) => (
              <div key={r.id} className="flex items-center gap-3 rounded border border-gray-200 p-3">
                <span className="text-xl font-bold text-gray-300 w-8 text-center">{i + 1}</span>
                <div className="flex-1">
                  <p className="font-semibold">{r.name}</p>
                  <p className="text-sm text-gray-500">{r.position}</p>
                </div>
                <p className="text-lg font-bold text-blue-600">{r.hours}h</p>
              </div>
            ))}
          </div>
        )}
      </Modal>
    </div>
  );
}
