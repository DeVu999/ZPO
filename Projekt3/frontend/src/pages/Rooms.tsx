import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useFetch } from '../hooks/useFetch';
import { roomService } from '../services/roomService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Button } from '../components/Button';
import { Modal } from '../components/Modal';
import { Input } from '../components/Input';
import { Form } from '../components/Form';
import { ErrorMessage } from '../components/ErrorMessage';
import { PageLoading } from '../components/Loading';
import { useForm } from 'react-hook-form';
import { required } from '../utils/validators';
import type { Room } from '../types/Room';

interface BookingFormData {
  title: string;
  start_time: string;
  end_time: string;
}

export function Rooms() {
  const { isAuthenticated } = useAuth();
  const { data: rooms, isLoading, error, refetch } = useFetch(
    (_signal) => roomService.getAll(),
    []
  );
  const [selectedRoom, setSelectedRoom] = useState<Room | null>(null);
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingError, setBookingError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const methods = useForm<BookingFormData>({
    defaultValues: { title: '', start_time: '', end_time: '' },
  });

  const handleBook = async (data: BookingFormData) => {
    if (!selectedRoom) return;
    setBookingLoading(true);
    setBookingError(null);
    try {
      await roomService.createBooking({
        room_id: selectedRoom.id,
        title: data.title,
        start_time: new Date(data.start_time).toISOString(),
        end_time: new Date(data.end_time).toISOString(),
      });
      setSuccessMessage('Rezerwacja została utworzona pomyślnie!');
      setSelectedRoom(null);
      methods.reset();
    } catch (err) {
      setBookingError(
        err instanceof Error ? err.message : 'Błąd rezerwacji'
      );
    } finally {
      setBookingLoading(false);
    }
  };

  const openBooking = (room: Room) => {
    setSelectedRoom(room);
    setBookingError(null);
    setSuccessMessage(null);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Text variant="h1">Sale</Text>
          <Text variant="body">Przeglądaj dostępne sale i rezerwuj terminy.</Text>
        </div>
        <Button variant="secondary" onClick={refetch}>
          Odśwież
        </Button>
      </div>

      <ErrorMessage message={error} onRetry={refetch} />

      {isLoading ? (
        <PageLoading />
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {(rooms ?? []).map((room) => (
            <Card key={room.id}>
              <CardHeader>
                <Text variant="h3">{room.name}</Text>
              </CardHeader>
              <CardBody className="space-y-3">
                <div>
                  <Text variant="small" className="font-medium">
                    Pojemność: {room.capacity} osób
                  </Text>
                </div>
                <Text variant="body">
                  {room.description || 'Brak opisu'}
                </Text>
                {isAuthenticated && (
                  <Button
                    variant="primary"
                    className="w-full"
                    onClick={() => openBooking(room)}
                  >
                    Rezerwuj
                  </Button>
                )}
              </CardBody>
            </Card>
          ))}
          {(!rooms || rooms.length === 0) && (
            <div className="col-span-full py-8 text-center text-sm text-gray-500">
              Brak dostępnych sal.
            </div>
          )}
        </div>
      )}

      <Modal
        isOpen={!!selectedRoom}
        onClose={() => {
          setSelectedRoom(null);
          setBookingError(null);
          setSuccessMessage(null);
        }}
        title={`Rezerwacja: ${selectedRoom?.name ?? ''}`}
      >
        {successMessage ? (
          <div className="space-y-4">
            <p className="rounded-lg bg-green-50 p-3 text-sm text-green-700">
              {successMessage}
            </p>
            <Button
              variant="primary"
              className="w-full"
              onClick={() => setSelectedRoom(null)}
            >
              OK
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <ErrorMessage message={bookingError} />

            <Form methods={methods} onSubmit={handleBook}>
              <Input
                name="title"
                label="Tytuł rezerwacji"
                placeholder="Np. Spotkanie zespołu"
                rules={{ validate: { required } }}
              />

              <Input
                name="start_time"
                type="datetime-local"
                label="Data i godzina rozpoczęcia"
                rules={{ validate: { required } }}
              />

              <Input
                name="end_time"
                type="datetime-local"
                label="Data i godzina zakończenia"
                rules={{ validate: { required } }}
              />

              <Button
                type="submit"
                variant="primary"
                isLoading={bookingLoading}
                className="w-full"
              >
                Potwierdź rezerwację
              </Button>
            </Form>
          </div>
        )}
      </Modal>
    </div>
  );
}
