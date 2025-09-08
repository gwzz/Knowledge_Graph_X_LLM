'use client';

import React, { useState } from 'react';
import { Filter, X, Plus, Download } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Collapsible, CollapsibleTrigger, CollapsibleContent } from '@/components/ui/collapsible'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { FilterCondition, Column } from '@/types';
import { cn } from '@/lib/utils';

interface FilterPanelProps {
  columns: Column[];
  filters: FilterCondition[];
  onFiltersChange: (filters: FilterCondition[]) => void;
  onExport: (format: 'csv' | 'json') => void;
  showFilters: boolean;
  onToggleFilters: () => void;
}

const OPERATORS = [
  { value: 'equals', label: 'Equals' },
  { value: 'contains', label: 'Contains' },
  { value: 'startsWith', label: 'Starts with' },
  { value: 'endsWith', label: 'Ends with' },
  { value: 'greater', label: 'Greater than' },
  { value: 'less', label: 'Less than' },
  { value: 'between', label: 'Between' },
] as const;

export function FilterPanel({ 
  columns, 
  filters, 
  onFiltersChange, 
  onExport, 
  showFilters, 
  onToggleFilters 
}: FilterPanelProps) {
  const [newFilter, setNewFilter] = useState<Partial<FilterCondition>>({});

  const addFilter = () => {
    if (newFilter.column && newFilter.operator && newFilter.value !== undefined) {
      onFiltersChange([...filters, newFilter as FilterCondition]);
      setNewFilter({});
    }
  };

  const removeFilter = (index: number) => {
    onFiltersChange(filters.filter((_, i) => i !== index));
  };

  const updateFilter = (index: number, updates: Partial<FilterCondition>) => {
    const updatedFilters = filters.map((filter, i) => 
      i === index ? { ...filter, ...updates } : filter
    );
    onFiltersChange(updatedFilters);
  };

  return (
    <div className="space-y-4">
      {/* Filter Controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant="outline"
            size="sm"
            onClick={onToggleFilters}
            className={cn(
              "transition-colors duration-200",
              showFilters && "bg-blue-50 border-blue-200 text-blue-700"
            )}
          >
            <Filter className="w-4 h-4 mr-2" />
            Filters
            {filters.length > 0 && (
              <Badge variant="secondary" className="ml-2 bg-blue-100 text-blue-700">
                {filters.length}
              </Badge>
            )}
          </Button>
          
          {filters.length > 0 && (
            <div className="flex items-center space-x-2">
              {filters.slice(0, 3).map((filter, index) => (
                <Badge 
                  key={index} 
                  variant="outline" 
                  className="text-xs bg-gray-50"
                >
                  {filter.column} {filter.operator} {
                    Array.isArray(filter.value) 
                      ? `${filter.value[0]} - ${filter.value[1]}`
                      : filter.value
                  }
                  <button
                    onClick={() => removeFilter(index)}
                    className="ml-1 hover:text-red-600"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </Badge>
              ))}
              {filters.length > 3 && (
                <Badge variant="outline" className="text-xs bg-gray-50">
                  +{filters.length - 3} more
                </Badge>
              )}
            </div>
          )}
        </div>

        {/* <div className="flex items-center space-x-2">
          <Select onValueChange={(format) => onExport(format as 'csv' | 'json')}>
            <SelectTrigger>
              <Button variant="outline" size="sm">
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="csv">CSV</SelectItem>
              <SelectItem value="json">JSON</SelectItem>
            </SelectContent>
          </Select>
        </div> */}
      </div>

      {/* Filter Builder */}
      {showFilters && (
        <Card>
          <CardContent className="p-4 space-y-4">
            {/* Existing Filters */}
            {filters.length > 0 && (
              <div className="space-y-3">
                <h4 className="text-sm font-medium text-gray-900">Active Filters</h4>
                {filters.map((filter, index) => (
                  <div key={index} className="flex items-center space-x-2 p-3 bg-gray-50 rounded-md">
                    <Select 
                      value={filter.column} 
                      onValueChange={(value) => updateFilter(index, { column: value })}
                    >
                      <SelectTrigger className="w-40">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {columns.map((column) => (
                          <SelectItem key={column.name} value={column.name}>
                            {column.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>

                    <Select 
                      value={filter.operator} 
                      onValueChange={(value) => updateFilter(index, { operator: value as any })}
                    >
                      <SelectTrigger className="w-32">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {OPERATORS.map((op) => (
                          <SelectItem key={op.value} value={op.value}>
                            {op.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>

                    {filter.operator === 'between' ? (
                      <div className="flex items-center space-x-2">
                        <Input
                          placeholder="From"
                          value={Array.isArray(filter.value) ? filter.value[0] : ''}
                          onChange={(e) => updateFilter(index, { 
                            value: [e.target.value, Array.isArray(filter.value) ? filter.value[1] : ''] 
                          })}
                          className="w-20"
                        />
                        <span className="text-gray-500">-</span>
                        <Input
                          placeholder="To"
                          value={Array.isArray(filter.value) ? filter.value[1] : ''}
                          onChange={(e) => updateFilter(index, { 
                            value: [Array.isArray(filter.value) ? filter.value[0] : '', e.target.value] 
                          })}
                          className="w-20"
                        />
                      </div>
                    ) : (
                      <Input
                        placeholder="Value"
                        value={Array.isArray(filter.value) ? '' : filter.value}
                        onChange={(e) => updateFilter(index, { value: e.target.value })}
                        className="flex-1"
                      />
                    )}

                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeFilter(index)}
                      className="hover:bg-red-50 hover:text-red-600"
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                ))}
              </div>
            )}

            {/* Add New Filter */}
            <div className="border-t pt-4">
              <h4 className="text-sm font-medium text-gray-900 mb-3">Add Filter</h4>
              <div className="flex items-center space-x-2">
                <Select 
                  value={newFilter.column || ''} 
                  onValueChange={(value) => setNewFilter({ ...newFilter, column: value })}
                >
                  <SelectTrigger className="w-40">
                    <SelectValue placeholder="Column" />
                  </SelectTrigger>
                  <SelectContent>
                    {columns.map((column) => (
                      <SelectItem key={column.name} value={column.name}>
                        {column.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Select 
                  value={newFilter.operator || ''} 
                  onValueChange={(value) => setNewFilter({ ...newFilter, operator: value as any })}
                >
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="Operator" />
                  </SelectTrigger>
                  <SelectContent>
                    {OPERATORS.map((op) => (
                      <SelectItem key={op.value} value={op.value}>
                        {op.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Input
                  placeholder="Value"
                  value={newFilter.value || ''}
                  onChange={(e) => setNewFilter({ ...newFilter, value: e.target.value })}
                  className="flex-1"
                />

                <Button
                  onClick={addFilter}
                  disabled={!newFilter.column || !newFilter.operator || !newFilter.value}
                  size="sm"
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  <Plus className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

interface TableListItemProps {
  table: Table;
  isSelected: boolean;
  onClick: () => void;
  formatRecordCount: (count: number) => string;
}

function TableListItem({ table, isSelected, onClick, formatRecordCount }: TableListItemProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "w-full text-left p-3 rounded-md transition-all duration-200",
        "hover:bg-gray-50 hover:shadow-sm border",
        isSelected
          ? "bg-blue-50 border-blue-200 shadow-sm"
          : "border-transparent hover:border-gray-200"
      )}
    >
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
          "text-xs font-medium px-2 py-1 rounded-full ml-2",
          isSelected
            ? "bg-blue-100 text-blue-700"
            : "bg-gray-100 text-gray-600"
        )}>
          {formatRecordCount(table.recordCount)}
        </div>
      </div>
    </button>
  );
}