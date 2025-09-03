export interface Table {
  name: string;
  displayName: string;
  recordCount: number;
}

export interface Column {
  name: string;
  type: string;
  nullable: boolean;
  primaryKey?: boolean;
}

export interface TableSchema {
  name: string;
  columns: Column[];
}

export interface PaginationInfo {
  page: number;
  pageSize: number;
  totalRecords: number;
  totalPages: number;
}

export interface FilterCondition {
  column: string;
  operator: 'equals' | 'contains' | 'startsWith' | 'endsWith' | 'greater' | 'less' | 'between';
  value: string | number | [string | number, string | number];
}

export interface SortCondition {
  column: string;
  direction: 'asc' | 'desc';
}

export interface DataResponse {
  data: Record<string, any>[];
  pagination: PaginationInfo;
  schema: TableSchema;
}

export interface ApiError {
  message: string;
  details?: string;
}