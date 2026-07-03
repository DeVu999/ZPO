import type { ReactNode } from 'react';

interface TextProps {
  children: ReactNode;
  variant?: 'h1' | 'h2' | 'h3' | 'body' | 'small';
  className?: string;
}

const variants: Record<string, string> = {
  h1: 'text-2xl font-bold text-gray-900',
  h2: 'text-xl font-semibold text-gray-900',
  h3: 'text-lg font-medium text-gray-900',
  body: 'text-sm text-gray-600',
  small: 'text-xs text-gray-500',
};

export function Text({ children, variant = 'body', className = '' }: TextProps) {
  const Tag = variant === 'h1' ? 'h1' : variant === 'h2' ? 'h2' : variant === 'h3' ? 'h3' : 'p';

  return (
    <Tag className={`${variants[variant]} ${className}`}>
      {children}
    </Tag>
  );
}
