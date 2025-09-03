'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import type { Table } from '@/types';

interface UseTablesReturn {
  tables: Table[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useTables(): UseTablesReturn {
  const [tables, setTables] = useState<Table[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTables = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.getTables();
      setTables(response);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch tables';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTables();
  }, []);

  const refetch = () => {
    fetchTables();
  };

  return { tables, loading, error, refetch };
}