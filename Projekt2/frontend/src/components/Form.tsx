import type { ReactNode } from 'react';
import type { FieldValues, UseFormReturn, SubmitHandler } from 'react-hook-form';
import { FormProvider } from 'react-hook-form';

interface FormProps<T extends FieldValues> {
  methods: UseFormReturn<T>;
  onSubmit: SubmitHandler<T>;
  children: ReactNode;
  className?: string;
}

export function Form<T extends FieldValues>({
  methods,
  onSubmit,
  children,
  className = '',
}: FormProps<T>) {
  return (
    <FormProvider {...methods}>
      <form
        onSubmit={methods.handleSubmit(onSubmit)}
        className={`space-y-4 ${className}`}
        noValidate
      >
        {children}
      </form>
    </FormProvider>
  );
}
