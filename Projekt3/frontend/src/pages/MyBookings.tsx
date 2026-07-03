import { useState } from 'react';
import { useFetch } from '../hooks/useFetch';
import { roomService } from '../services/roomService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Table } from '../components/Table';
import { Button } from '../components/Button';
import { ErrorMessage } from '../components/ErrorMessage';
import { PageLoading } from '../components/Loading';
import { Modal } from '../components/Modal';
import { formatDateTime } from '../utils/helpers';
import type { Booking } from '../types/Room';

export function MyBookings() {
  const {
    data: bookings,
    isLoading,
    error,
    refetch,
  } = useFetch((_signal) => roomService.getAllBookings(), []);

  const [deleteTarget, setDeleteTarget] = useState<Booking | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  const handleDelete = async () => {
    if (!deleteTarget) return;
    setDeleteLoading(true);
    setDeleteError(null);
    try {
      await roomService.deleteBooking(deleteTarget.id);
      setDeleteTarget(null);
      refetch();
    } catch (err) {
      setDeleteError(err instanceof Error ? err.message : 'Błąd usuwania');
    } finally {
      setDeleteLoading(false);
    }
  };

  const columns = [
    { key: 'id', header: 'ID' },
    { key: 'title', header: 'Tytuł' },
    {
      key: 'room_id',
      header: 'Sala ID',
      render: (item: Booking) => item.room_id,
    },
    {
      key: 'start_time',
      header: 'Od',
      render: (item: Booking) => formatDateTime(item.start_time),
    },
    {
      key: 'end_time',
      header: 'Do',
      render: (item: Booking) => formatDateTime(item.end_time),
    },
    {
      key: 'actions',
      header: 'Akcje',
      render: (item: Booking) => (
        <Button
          variant="danger"
          onClick={(e) => {
            e.stopPropagation();
            setDeleteTarget(item);
          }}
        >
          Anuluj
        </Button>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Text variant="h1">Moje Rezerwacje</Text>
          <Text variant="body">
            Lista Twoich rezerwacji sal.
          </Text>
        </div>
        <Button variant="secondary" onClick={refetch}>
          Odśwież
        </Button>
      </div>

      <Card>
        <CardHeader>
          <Text variant="h3">Rezerwacje</Text>
        </CardHeader>
        <CardBody>
          <ErrorMessage message={error} onRetry={refetch} />
          {isLoading ? (
            <PageLoading />
          ) : (
            <Table
              columns={columns}
              data={bookings ?? []}
              emptyMessage="Brak rezerwacji"
            />
          )}
        </CardBody>
      </Card>

      <Modal
        isOpen={!!deleteTarget}
        onClose={() => {
          setDeleteTarget(null);
          setDeleteError(null);
        }}
        title="Anuluj rezerwację"
      >
        <div className="space-y-4">
          <Text variant="body">
            Czy na pewno chcesz anulować rezerwację "{deleteTarget?.title}"?
          </Text>

          <ErrorMessage message={deleteError} />

          <div className="flex gap-3 pt-2">
            <Button
              variant="danger"
              isLoading={deleteLoading}
              onClick={handleDelete}
            >
              Anuluj rezerwację
            </Button>
            <Button
              variant="ghost"
              onClick={() => {
                setDeleteTarget(null);
                setDeleteError(null);
              }}
            >
              Zamknij
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
