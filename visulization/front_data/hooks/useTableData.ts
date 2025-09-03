'use client';

import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '@/lib/api';
import type { DataResponse, FilterCondition, SortCondition, ApiError } from '@/types';

interface UseTableDataProps {
  tableName: string | null;
  page: number;
  pageSize: number;
  filters: FilterCondition[];
  sort?: SortCondition;
}

interface UseTableDataReturn {
  data: DataResponse | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useTableData({
  tableName,
  page,
  pageSize,
  filters,
  sort,
}: UseTableDataProps): UseTableDataReturn {
  const [data, setData] = useState<DataResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    if (!tableName) {
      setData(null);
      setLoading(false);
      setError(null);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.getTableData(tableName, page, pageSize, filters, sort);
      setData(response);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch data';
      setError(errorMessage);
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [tableName, page, pageSize, filters, sort]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const refetch = useCallback(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch };
}