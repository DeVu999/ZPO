import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useFetch } from '../hooks/useFetch';
import { classService } from '../services/classService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Button } from '../components/Button';
import { ErrorMessage } from '../components/ErrorMessage';
import { PageLoading } from '../components/Loading';
import { formatDateTime } from '../utils/helpers';

export function MyClasses() {
  const { user } = useAuth();
  const {
    data: signups,
    isLoading,
    error,
    refetch,
  } = useFetch((_signal) => classService.getMyClasses(), []);

  const [cancelLoading, setCancelLoading] = useState<number | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  const handleCancel = async (classId: number) => {
    setCancelLoading(classId);
    setActionError(null);
    try {
      await classService.cancelSignup(classId);
      refetch();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Błąd anulowania');
    } finally {
      setCancelLoading(null);
    }
  };

  if (!user) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Text variant="h1">Moje Zajęcia</Text>
          <Text variant="body">Lista zajęć na które jesteś zapisany.</Text>
        </div>
        <Button variant="secondary" onClick={refetch}>
          Odśwież
        </Button>
      </div>

      <ErrorMessage message={error ?? actionError} onRetry={refetch} />

      {isLoading ? (
        <PageLoading />
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {(signups ?? []).map((signup) => (
            <Card key={signup.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <Text variant="h3">{signup.fitness_class.name}</Text>
                  <span className={`rounded px-2 py-1 text-xs font-medium ${
                    signup.is_waitlisted
                      ? 'bg-yellow-100 text-yellow-700'
                      : 'bg-green-100 text-green-700'
                  }`}>
                    {signup.is_waitlisted ? 'Rezerwowa' : 'Aktywne'}
                  </span>
                </div>
              </CardHeader>
              <CardBody className="space-y-3">
                <Text variant="body">{signup.fitness_class.description || 'Brak opisu'}</Text>
                <div className="space-y-1">
                  <Text variant="small">Prowadzący: {signup.fitness_class.instructor}</Text>
                  <Text variant="small">Data: {formatDateTime(signup.fitness_class.datetime)}</Text>
                  <Text variant="small">
                    Miejsca: {signup.fitness_class.capacity - signup.fitness_class.free_spots}/{signup.fitness_class.capacity}
                  </Text>
                  <Text variant="small">Zapisano: {formatDateTime(signup.signed_up_at)}</Text>
                </div>
                <Button
                  variant="danger"
                  className="w-full"
                  isLoading={cancelLoading === signup.class_id}
                  onClick={() => handleCancel(signup.class_id)}
                >
                  Anuluj zapis
                </Button>
              </CardBody>
            </Card>
          ))}
          {(signups ?? []).length === 0 && (
            <div className="col-span-full py-8 text-center text-sm text-gray-500">
              Nie jesteś zapisany na żadne zajęcia.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
