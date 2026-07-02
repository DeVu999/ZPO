import type { ReactNode } from 'react';

interface CenterProps {
  children: ReactNode;
  className?: string;
}

export function Center({ children, className = '' }: CenterProps) {
  return (
    <div
      className={`flex min-h-screen items-center justify-center ${className}`}
    >
      {children}
    </div>
  );
}
