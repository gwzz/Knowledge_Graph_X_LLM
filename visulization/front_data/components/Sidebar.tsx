'use client';

import React, { useState } from 'react';
import { Search, Database, RefreshCw, ChevronRight } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Skeleton } from '@/components/ui/skeleton';
import { useTables } from '@/hooks/useTables';
import { cn } from '@/lib/utils';
import type { Table } from '@/types';

interface SidebarProps {
  selectedTable: string | null;
  onTableSelect: (tableName: string) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
}

export function Sidebar({ selectedTable, onTableSelect, collapsed, onToggleCollapse }: SidebarProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const { tables, loading, error, refetch } = useTables();
  const filteredTables = tables.filter(table =>
    table.displayName.toLowerCase().includes(searchQuery.toLowerCase()) ||
    table.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const formatRecordCount = (count: number): string => {
    if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`;
    if (count >= 1000) return `${(count / 1000).toFixed(1)}K`;
    return count.toString();
  };

  return (
    <div className={cn(
      "bg-white border-r border-gray-200 transition-all duration-300 ease-in-out flex flex-col h-full",
      collapsed ? "w-16" : "w-80"
    )}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          {!collapsed && (
            <div className="flex items-center space-x-2">
              <Database className="w-6 h-6 text-blue-600" />
              <h1 className="text-lg font-semibold text-gray-900">Database Explorer</h1>
            </div>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={onToggleCollapse}
            className="hover:bg-gray-100"
          >
            <ChevronRight className={cn(
              "w-4 h-4 transition-transform duration-200",
              collapsed ? "rotate-0" : "rotate-180"
            )} />
          </Button>
        </div>

        {!collapsed && (
          <div className="mt-4 space-y-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <Input
                placeholder="Search tables..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9"
              />
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={refetch}
              disabled={loading}
              className="w-full"
            >
              <RefreshCw className={cn("w-4 h-4 mr-2", loading && "animate-spin")} />
              Refresh
            </Button>
          </div>
        )}
      </div>

      {/* Tables List */}
      <ScrollArea className="flex-1">
        <div className="p-2">
          {loading ? (
            <div className="space-y-2">
              {[...Array(6)].map((_, i) => (
                <Skeleton key={i} className={cn(
                  "rounded-md",
                  collapsed ? "h-10 w-10" : "h-12 w-full"
                )} />
              ))}
            </div>
          ) : error ? (
            <div className={cn(
              "text-center py-8",
              collapsed ? "px-2" : "px-4"
            )}>
              <p className={cn(
                "text-sm text-red-600",
                collapsed && "hidden"
              )}>
                {error}
              </p>
              {collapsed && (
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mx-auto">
                  <Database className="w-4 h-4 text-red-600" />
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-1">
              {filteredTables.map((table) => (
                <TableItem
                  key={table.name}
                  table={table}
                  isSelected={selectedTable === table.name}
                  onClick={() => onTableSelect(table.name)}
                  collapsed={collapsed}
                  formatRecordCount={formatRecordCount}
                />
              ))}
              {filteredTables.length === 0 && searchQuery && (
                <div className={cn(
                  "text-center py-8",
                  collapsed && "hidden"
                )}>
                  <p className="text-sm text-gray-500">No tables found matching "{searchQuery}"</p>
                </div>
              )}
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

interface TableItemProps {
  table: Table;
  isSelected: boolean;
  onClick: () => void;
  collapsed: boolean;
  formatRecordCount: (count: number) => string;
}

function TableItem({ table, isSelected, onClick, collapsed, formatRecordCount }: TableItemProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "w-full text-left p-3 rounded-md transition-all duration-200 group",
        "hover:bg-gray-50 hover:shadow-sm",
        isSelected
          ? "bg-blue-50 border border-blue-200 shadow-sm"
          : "hover:bg-gray-50",
        collapsed && "flex justify-center p-2"
      )}
    >
      {collapsed ? (
        <div className={cn(
          "w-8 h-8 rounded-md flex items-center justify-center text-xs font-medium",
          isSelected
            ? "bg-blue-600 text-white"
            : "bg-gray-100 text-gray-600 group-hover:bg-gray-200"
        )}>
          {table.displayName.charAt(0).toUpperCase()}
        </div>
      ) : (
        <div className="flex items-center justify-between">
          <div className="flex-1 min-w-0">
            <p className={cn(
              "font-medium text-sm truncate",
              isSelected ? "text-blue-900" : "text-gray-900"
            )}>
              {table.displayName}
            </p>
            <p className={cn(
              "text-xs truncate mt-1",
              isSelected ? "text-blue-600" : "text-gray-500"
            )}>
              {table.name}
            </p>
          </div>
          <div className={cn(
            "text-xs font-medium px-2 py-1 rounded-full",
            isSelected
              ? "bg-blue-100 text-blue-700"
              : "bg-gray-100 text-gray-600"
          )}>
            {formatRecordCount(table.recordCount)}
          </div>
        </div>
      )}
    </button>
  );
}