import { useState } from 'react';
import { useFetch } from '../hooks/useFetch';
import { movieService } from '../services/movieService';
import { Card, CardBody, CardHeader } from '../components/Card';
import { Text } from '../components/Text';
import { ErrorMessage } from '../components/ErrorMessage';
import { PageLoading } from '../components/Loading';

const GENRES = ['', 'Akcja', 'Komedia', 'Dramat', 'Horror', 'Sci-Fi', 'Thriller', 'Romans'];

export function TopMovies() {
  const [genre, setGenre] = useState('');

  const { data, isLoading, error, refetch } = useFetch(
    (_signal) => movieService.getTop(genre || undefined, 10),
    [genre]
  );

  const movies = data ?? [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <Text variant="h1">Top Filmy</Text>
          <Text variant="body">Najlepiej oceniane filmy.</Text>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-600">Gatunek:</label>
          <select
            value={genre}
            onChange={(e) => setGenre(e.target.value)}
            className="rounded-lg border border-gray-300 px-3 py-2 text-sm"
          >
            <option value="">Wszystkie</option>
            {GENRES.filter(Boolean).map((g) => (
              <option key={g} value={g}>{g}</option>
            ))}
          </select>
        </div>
      </div>

      <Card>
        <CardHeader>
          <Text variant="h3">
            Ranking {genre ? `- ${genre}` : 'ogólny'}
          </Text>
        </CardHeader>
        <CardBody>
          <ErrorMessage message={error} onRetry={refetch} />
          {isLoading ? (
            <PageLoading />
          ) : movies.length === 0 ? (
            <p className="py-8 text-center text-sm text-gray-500">
              Brak ocenionych filmów{genre ? ` w gatunku ${genre}` : ''}.
            </p>
          ) : (
            <div className="space-y-3">
              {movies.map((m, i) => (
                <div
                  key={m.id}
                  className="flex items-center gap-4 rounded-lg border border-gray-100 p-4"
                >
                  <span className="text-2xl font-bold text-gray-300 w-8 text-center">
                    {i + 1}
                  </span>
                  <div className="flex-1">
                    <p className="font-semibold text-gray-900">{m.title}</p>
                    <p className="text-sm text-gray-500">
                      {m.description || '-'} &middot; {m.genre}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-xl font-bold text-yellow-500">
                      {m.avg.toFixed(1)}
                    </p>
                    <p className="text-xs text-gray-400">
                      {m.count} {m.count === 1 ? 'ocena' : 'ocen'}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
}
