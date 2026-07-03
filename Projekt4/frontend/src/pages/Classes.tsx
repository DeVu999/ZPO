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
import type { FitnessClass, MyClassSignup } from '../types/Fitness';

export function Classes() {
  const { isAuthenticated } = useAuth();
  const {
    data: classes,
    isLoading,
    error,
    refetch,
  } = useFetch((_signal) => classService.getAll(), []);

  const {
    data: mySignups,
    refetch: refetchMyClasses,
  } = useFetch((_signal) => isAuthenticated ? classService.getMyClasses() : Promise.resolve([]), [isAuthenticated]);

  const [actionLoading, setActionLoading] = useState<number | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  const signups = mySignups ?? [];

  const getMySignup = (classId: number): MyClassSignup | undefined =>
    signups.find((s) => s.class_id === classId);

  const handleSignup = async (classItem: FitnessClass) => {
    setActionLoading(classItem.id);
    setActionError(null);
    try {
      if (classItem.free_spots > 0) {
        await classService.signup({ class_id: classItem.id });
      } else {
        await classService.signup({ class_id: classItem.id });
      }
      refetch();
      refetchMyClasses();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Błąd zapisu');
    } finally {
      setActionLoading(null);
    }
  };

  const handleCancel = async (classItem: FitnessClass) => {
    setActionLoading(classItem.id);
    setActionError(null);
    try {
      await classService.cancelSignup(classItem.id);
      refetch();
      refetchMyClasses();
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Błąd anulowania');
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Text variant="h1">Zajęcia Fitness</Text>
          <Text variant="body">Przeglądaj dostępne zajęcia i zapisz się.</Text>
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
          {(classes ?? []).map((item) => {
            const signup = getMySignup(item.id);
            const isSignedUp = !!signup;
            const isWaitlisted = signup?.is_waitlisted ?? false;

            return (
              <Card key={item.id}>
                <CardHeader>
                  <Text variant="h3">{item.name}</Text>
                </CardHeader>
                <CardBody className="space-y-3">
                  <Text variant="body">{item.description || 'Brak opisu'}</Text>
                  <div className="space-y-1">
                    <Text variant="small">Prowadzący: {item.instructor}</Text>
                    <Text variant="small">Data: {formatDateTime(item.datetime)}</Text>
                    <Text variant="small">
                      Miejsca: {item.capacity - item.free_spots}/{item.capacity}
                      {item.free_spots > 0 ? (
                        <span className="ml-1 text-green-600">
                          ({item.free_spots} wolnych)
                        </span>
                      ) : (
                        <span className="ml-1 text-red-600">(brak miejsc)</span>
                      )}
                    </Text>
                  </div>

                  {isSignedUp ? (
                    <div className="space-y-2">
                      <span className={`inline-block rounded px-2 py-1 text-xs font-medium ${
                        isWaitlisted
                          ? 'bg-yellow-100 text-yellow-700'
                          : 'bg-green-100 text-green-700'
                      }`}>
                        {isWaitlisted ? 'Lista rezerwowa' : 'Jesteś zapisany'}
                      </span>
                      <Button
                        variant="danger"
                        className="w-full"
                        isLoading={actionLoading === item.id}
                        onClick={() => handleCancel(item)}
                      >
                        Anuluj zapis
                      </Button>
                    </div>
                  ) : (
                    <Button
                      variant={item.free_spots > 0 ? 'primary' : 'secondary'}
                      className="w-full"
                      isLoading={actionLoading === item.id}
                      onClick={() => handleSignup(item)}
                      disabled={!isAuthenticated}
                      title={!isAuthenticated ? 'Zaloguj się aby zapisać' : undefined}
                    >
                      {item.free_spots > 0 ? 'Zapisz się' : 'Lista rezerwowa'}
                    </Button>
                  )}
                </CardBody>
              </Card>
            );
          })}
          {(classes ?? []).length === 0 && (
            <div className="col-span-full py-8 text-center text-sm text-gray-500">
              Brak dostępnych zajęć.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
