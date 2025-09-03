const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ 
          message: `HTTP ${response.status}: ${response.statusText}` 
        }));
        throw new Error(errorData.message || `Request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred');
    }
  }

  async getTables(): Promise<Table[]> {
    return this.request<Table[]>('/knowledge/tables');
  }

  async getTableSchema(tableName: string): Promise<TableSchema> {
    return this.request<TableSchema>(`/knowledge/get_table_schema/${tableName}`);
  }

  async getTableData(
    tableName: string,
    page: number = 1,
    pageSize: number = 50,
    filters: FilterCondition[] = [],
    sort?: SortCondition
  ): Promise<DataResponse> {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: pageSize.toString(),
    });

    if (filters.length > 0) {
      params.append('filters', JSON.stringify(filters));
    }

    if (sort) {
      params.append('sort', JSON.stringify(sort));
    }

    return this.request<DataResponse>(`/knowledge/get_table_data/${tableName}?${params}`);
  }

  async exportTableData(
    tableName: string,
    filters: FilterCondition[] = [],
    sort?: SortCondition,
    format: 'csv' | 'json' = 'csv'
  ): Promise<Blob> {
    const params = new URLSearchParams({ format });

    if (filters.length > 0) {
      params.append('filters', JSON.stringify(filters));
    }

    if (sort) {
      params.append('sort', JSON.stringify(sort));
    }

    const response = await fetch(`${this.baseUrl}/tables/${tableName}/export?${params}`);
    
    if (!response.ok) {
      throw new Error(`Export failed with status ${response.status}`);
    }

    return response.blob();
  }
}

export const apiClient = new ApiClient();