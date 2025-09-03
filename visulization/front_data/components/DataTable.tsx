'use client';

import React, { useState } from 'react';
import { ChevronUp, ChevronDown, MoreHorizontal, Eye, Copy } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import type { DataResponse, SortCondition, Column } from '@/types';

interface DataTableProps {
  data: DataResponse | null;
  loading: boolean;
  error: string | null;
  sort?: SortCondition;
  onSortChange: (sort: SortCondition) => void;
}

export function DataTable({ data, loading, error, sort, onSortChange }: DataTableProps) {
  const [selectedCell, setSelectedCell] = useState<{ row: number; column: string; value: any } | null>(null);

  if (loading) {
    return <DataTableSkeleton />;
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg border border-gray-200">
        <div className="text-center">
          <p className="text-gray-500 mb-2">Failed to load data</p>
          <p className="text-sm text-gray-400">{error}</p>
        </div>
      </div>
    );
  }

  if (!data || data.data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg border border-gray-200">
        <div className="text-center">
          <p className="text-gray-500">No data available</p>
          <p className="text-sm text-gray-400 mt-1">
            {data?.pagination.totalRecords === 0 
              ? "This table contains no records" 
              : "No records match the current filters"
            }
          </p>
        </div>
      </div>
    );
  }

  const { schema, data: records } = data;

  const handleSort = (columnName: string) => {
    const newDirection = 
      sort?.column === columnName && sort.direction === 'asc' ? 'desc' : 'asc';
    onSortChange({ column: columnName, direction: newDirection });
  };

  const formatCellValue = (value: any, column: Column): React.ReactNode => {
    if (value === null || value === undefined) {
      return <span className="text-gray-400 italic">null</span>;
    }

    if (column.type === 'boolean') {
      return (
        <Badge variant={value ? "default" : "secondary"} className="text-xs">
          {value ? 'true' : 'false'}
        </Badge>
      );
    }

    if (column.type.includes('timestamp') || column.type.includes('date')) {
      try {
        return new Date(value).toLocaleString();
      } catch {
        return value;
      }
    }

    if (typeof value === 'object') {
      return (
        <span className="text-blue-600 cursor-pointer" onClick={() => 
          setSelectedCell({ row: 0, column: column.name, value })
        }>
          {JSON.stringify(value).substring(0, 50)}...
        </span>
      );
    }

    const stringValue = String(value);
    if (stringValue.length > 100) {
      return (
        <span
          className="cursor-pointer hover:text-blue-600"
          onClick={() => setSelectedCell({ row: 0, column: column.name, value })}
        >
          {stringValue.substring(0, 100)}...
        </span>
      );
    }

    return stringValue;
  };

  const copyToClipboard = (value: any) => {
    navigator.clipboard.writeText(typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value));
  };

  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-gray-200 overflow-hidden bg-white shadow-sm">
        <ScrollArea className="h-[600px]">
          <Table>
            <TableHeader className="bg-gray-50 sticky top-0 z-10">
              <TableRow>
                {schema.columns.map((column) => (
                  <TableHead 
                    key={column.name}
                    className="font-semibold text-gray-900 border-b border-gray-200"
                  >
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleSort(column.name)}
                      className="h-auto p-0 hover:bg-transparent font-semibold text-left justify-start w-full"
                    >
                      <div className="flex items-center space-x-2">
                        <span>{column.name}</span>
                        {column.primaryKey && (
                          <Badge variant="outline" className="text-xs bg-yellow-50 text-yellow-700 border-yellow-200">
                            PK
                          </Badge>
                        )}
                        <div className="flex flex-col">
                          <ChevronUp 
                            className={cn(
                              "w-3 h-3 -mb-1",
                              sort?.column === column.name && sort.direction === 'asc'
                                ? "text-blue-600"
                                : "text-gray-300"
                            )} 
                          />
                          <ChevronDown 
                            className={cn(
                              "w-3 h-3",
                              sort?.column === column.name && sort.direction === 'desc'
                                ? "text-blue-600"
                                : "text-gray-300"
                            )} 
                          />
                        </div>
                      </div>
                    </Button>
                    <div className="text-xs text-gray-500 mt-1 font-normal">
                      {column.type}{column.nullable && ', nullable'}
                    </div>
                  </TableHead>
                ))}
                <TableHead className="w-12"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {records.map((record, rowIndex) => (
                <TableRow 
                  key={rowIndex}
                  className="hover:bg-gray-50 transition-colors duration-150"
                >
                  {schema.columns.map((column) => (
                    <TableCell 
                      key={column.name}
                      className="border-b border-gray-100 max-w-xs"
                    >
                      <div className="truncate">
                        {formatCellValue(record[column.name], column)}
                      </div>
                    </TableCell>
                  ))}
                  <TableCell className="border-b border-gray-100">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                          <MoreHorizontal className="w-4 h-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem
                          onClick={() => setSelectedCell({ 
                            row: rowIndex, 
                            column: 'full_record', 
                            value: record 
                          })}
                        >
                          <Eye className="w-4 h-4 mr-2" />
                          View Record
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => copyToClipboard(record)}
                        >
                          <Copy className="w-4 h-4 mr-2" />
                          Copy JSON
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </ScrollArea>
      </div>

      {/* Cell Detail Dialog */}
      <Dialog open={!!selectedCell} onOpenChange={() => setSelectedCell(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {selectedCell?.column === 'full_record' ? 'Full Record' : `Column: ${selectedCell?.column}`}
            </DialogTitle>
          </DialogHeader>
          <div className="mt-4">
            <ScrollArea className="h-96 w-full rounded-md border p-4">
              <pre className="text-sm whitespace-pre-wrap">
                {typeof selectedCell?.value === 'object'
                  ? JSON.stringify(selectedCell.value, null, 2)
                  : String(selectedCell?.value)
                }
              </pre>
            </ScrollArea>
            <div className="mt-4 flex justify-end">
              <Button
                variant="outline"
                size="sm"
                onClick={() => copyToClipboard(selectedCell?.value)}
              >
                <Copy className="w-4 h-4 mr-2" />
                Copy
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

function DataTableSkeleton() {
  return (
    <div className="rounded-lg border border-gray-200 overflow-hidden bg-white">
      <div className="p-4 border-b border-gray-200 bg-gray-50">
        <div className="flex space-x-4">
          {[...Array(5)].map((_, i) => (
            <Skeleton key={i} className="h-6 w-24" />
          ))}
        </div>
      </div>
      <div className="space-y-2 p-4">
        {[...Array(10)].map((_, i) => (
          <div key={i} className="flex space-x-4">
            {[...Array(5)].map((_, j) => (
              <Skeleton key={j} className="h-8 flex-1" />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}