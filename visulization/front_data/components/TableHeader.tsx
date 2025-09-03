'use client';

import React from 'react';
import { RefreshCw, Table } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import type { DataResponse } from '@/types';
import { cn } from '@/lib/utils';

interface TableHeaderProps {
  tableName: string | null;
  data: DataResponse | null;
  loading: boolean;
  onRefresh: () => void;
}

export function TableHeader({ tableName, data, loading, onRefresh }: TableHeaderProps) {
  if (!tableName) {
    return (
      <div className="flex items-center justify-center h-32 bg-gray-50 rounded-lg border border-gray-200">
        <div className="text-center">
          <Table className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500">Select a table to view data</p>
          <p className="text-sm text-gray-400 mt-1">Choose a table from the sidebar to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="flex items-center space-x-3">
            <h1 className="text-2xl font-bold text-gray-900">
              {data?.schema.name || tableName}
            </h1>
            {data && (
              <Badge variant="secondary" className="text-sm">
                {data.pagination.totalRecords.toLocaleString()} records
              </Badge>
            )}
          </div>
          
          {data && (
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <span>{data.schema.columns.length} columns</span>
              <span>•</span>
              <span>
                Page {data.pagination.page} of {data.pagination.totalPages}
              </span>
            </div>
          )}
        </div>

        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={onRefresh}
            disabled={loading}
            className="hover:bg-gray-50"
          >
            <RefreshCw className={cn("w-4 h-4 mr-2", loading && "animate-spin")} />
            Refresh
          </Button>
        </div>
      </div>
    </div>
  );
}