import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useFetch } from '../hooks/useFetch';
import { movieService } from '../services/movieService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { Table } from '../components/Table';
import { Button } from '../components/Button';
import { ErrorMessage } from '../components/ErrorMessage';
import { PageLoading } from '../components/Loading';
import { formatDate } from '../utils/helpers';
import type { Movie } from '../types/Movie';

export function Movies() {
  const { isAuthenticated } = useAuth();
  const { data: movies, isLoading, error, refetch } = useFetch(
    (_signal) => movieService.getAll(),
    []
  );
  const [ratingLoading, setRatingLoading] = useState<number | null>(null);

  const handleRate = async (movieId: number, score: number) => {
    setRatingLoading(movieId);
    try {
      await movieService.rate(movieId, score);
      refetch();
    } catch {
      // ignore
    } finally {
      setRatingLoading(null);
    }
  };

  const renderStars = (movie: Movie) => (
    <div className="flex items-center gap-1">
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          onClick={() => handleRate(movie.id, star)}
          disabled={!isAuthenticated || ratingLoading === movie.id}
          className={`text-lg ${
            star <= (movie.average_rating ?? 0)
              ? 'text-yellow-400'
              : 'text-gray-300'
          } hover:text-yellow-500 disabled:cursor-not-allowed`}
          title={isAuthenticated ? `Oceń na ${star}` : 'Zaloguj się aby ocenić'}
        >
          ★
        </button>
      ))}
      <span className="ml-2 text-sm text-gray-500">
        {movie.average_rating?.toFixed(1) ?? '-'} ({movie.rating_count})
      </span>
    </div>
  );

  const columns = [
    { key: 'id', header: 'ID' },
    { key: 'title', header: 'Tytuł' },
    {
      key: 'description',
      header: 'Opis',
      render: (item: Movie) => (
        <span className="max-w-xs truncate block">{item.description || '-'}</span>
      ),
    },
    {
      key: 'genre',
      header: 'Gatunek',
      render: (item: Movie) => (
        <span className="rounded bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-700">
          {item.genre}
        </span>
      ),
    },
    {
      key: 'rating',
      header: 'Ocena',
      render: (item: Movie) => renderStars(item),
    },
    {
      key: 'created_at',
      header: 'Dodano',
      render: (item: Movie) => formatDate(item.created_at),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Text variant="h1">Filmy</Text>
          <Text variant="body">Przeglądaj i oceniaj filmy w skali 1-5.</Text>
        </div>
        <Button variant="secondary" onClick={refetch}>
          Odśwież
        </Button>
      </div>

      <Card>
        <CardHeader>
          <Text variant="h3">Lista filmów</Text>
        </CardHeader>
        <CardBody>
          <ErrorMessage message={error} onRetry={refetch} />
          {isLoading ? (
            <PageLoading />
          ) : (
            <Table columns={columns} data={movies ?? []} />
          )}
        </CardBody>
      </Card>
    </div>
  );
}
