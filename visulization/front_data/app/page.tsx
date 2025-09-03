'use client';

import React, { useState, useCallback } from 'react';
import { Sidebar } from '@/components/Sidebar';
import { TableHeader } from '@/components/TableHeader';
import { FilterPanel } from '@/components/FilterPanel';
import { DataTable } from '@/components/DataTable';
import { Pagination } from '@/components/Pagination';
import { useTableData } from '@/hooks/useTableData';
import { apiClient } from '@/lib/api';
import type { FilterCondition, SortCondition } from '@/types';

export default function DatabaseManagementPlatform() {
  const [selectedTable, setSelectedTable] = useState<string | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);
  const [filters, setFilters] = useState<FilterCondition[]>([]);
  const [sort, setSort] = useState<SortCondition | undefined>();
  const [showFilters, setShowFilters] = useState(false);

  const { data, loading, error, refetch } = useTableData({
    tableName: selectedTable,
    page: currentPage,
    pageSize,
    filters,
    sort,
  });

  const handleTableSelect = useCallback((tableName: string) => {
    setSelectedTable(tableName);
    setCurrentPage(1);
    setFilters([]);
    setSort(undefined);
  }, []);

  const handlePageChange = useCallback((page: number) => {
    setCurrentPage(page);
  }, []);

  const handlePageSizeChange = useCallback((newPageSize: number) => {
    setPageSize(newPageSize);
    setCurrentPage(1);
  }, []);

  const handleFiltersChange = useCallback((newFilters: FilterCondition[]) => {
    setFilters(newFilters);
    setCurrentPage(1);
  }, []);

  const handleSortChange = useCallback((newSort: SortCondition) => {
    setSort(newSort);
    setCurrentPage(1);
  }, []);

  const handleExport = useCallback(async (format: 'csv' | 'json') => {
    if (!selectedTable) return;

    try {
      const blob = await apiClient.exportTableData(selectedTable, filters, sort, format);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${selectedTable}_export.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export failed:', error);
    }
  }, [selectedTable, filters, sort]);

  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      <Sidebar
        selectedTable={selectedTable}
        onTableSelect={handleTableSelect}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
      />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 p-6 space-y-6 overflow-auto">
          <TableHeader
            tableName={selectedTable}
            data={data}
            loading={loading}
            onRefresh={refetch}
          />

          {selectedTable && data && (
            <>
              <FilterPanel
                columns={data.schema.columns}
                filters={filters}
                onFiltersChange={handleFiltersChange}
                onExport={handleExport}
                showFilters={showFilters}
                onToggleFilters={() => setShowFilters(!showFilters)}
              />

              <DataTable
                data={data}
                loading={loading}
                error={error}
                sort={sort}
                onSortChange={handleSortChange}
              />

              {data.pagination.totalPages > 1 && (
                <Pagination
                  pagination={data.pagination}
                  onPageChange={handlePageChange}
                  onPageSizeChange={handlePageSizeChange}
                />
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}