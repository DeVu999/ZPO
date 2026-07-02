interface OutputProps {
  label?: string;
  value: string | number | null | undefined;
}

export function Output({ label, value }: OutputProps) {
  if (value === null || value === undefined) return null;

  return (
    <div className="space-y-1">
      {label && (
        <p className="text-sm font-medium text-gray-500">{label}</p>
      )}
      <p className="text-sm text-gray-900">{String(value)}</p>
    </div>
  );
}

export function OutputBlock({ label, value }: OutputProps) {
  if (value === null || value === undefined) return null;

  return (
    <div className="space-y-1">
      {label && (
        <p className="text-sm font-medium text-gray-500">{label}</p>
      )}
      <pre className="whitespace-pre-wrap rounded-lg bg-gray-50 p-3 text-sm text-gray-900">
        {String(value)}
      </pre>
    </div>
  );
}
