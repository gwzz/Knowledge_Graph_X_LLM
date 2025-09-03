# Database Management Platform

A modern, responsive database management platform built with Next.js and designed to work with FastAPI backends.

## Features

- **Dynamic Table Explorer**: Browse and select database tables from an intuitive sidebar
- **Advanced Data Viewer**: View table data with sortable columns and responsive design
- **Smart Filtering**: Apply multiple filters with various operators (equals, contains, greater than, etc.)
- **Pagination**: Navigate large datasets efficiently with customizable page sizes
- **Export Functionality**: Export filtered data in CSV or JSON formats
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Getting Started

1. **Configure API Connection**:
   ```bash
   cp .env.example .env.local
   ```
   Update `NEXT_PUBLIC_API_URL` with your FastAPI backend URL.

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Start Development Server**:
   ```bash
   npm run dev
   ```

## FastAPI Backend Requirements

Your FastAPI backend should implement the following endpoints:

### GET `/tables`
Returns list of available tables:
```json
[
  {
    "name": "users",
    "displayName": "Users",
    "recordCount": 1250
  }
]
```

### GET `/tables/{table_name}/schema`
Returns table schema:
```json
{
  "name": "users",
  "columns": [
    {
      "name": "id",
      "type": "integer",
      "nullable": false,
      "primaryKey": true
    },
    {
      "name": "email",
      "type": "varchar",
      "nullable": false
    }
  ]
}
```

### GET `/tables/{table_name}/data`
Returns paginated table data with optional filtering and sorting:

Query Parameters:
- `page`: Page number (default: 1)
- `page_size`: Records per page (default: 50)
- `filters`: JSON string of filter conditions
- `sort`: JSON string of sort condition

Response:
```json
{
  "data": [
    {"id": 1, "email": "user@example.com"},
    {"id": 2, "email": "admin@example.com"}
  ],
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "totalRecords": 1250,
    "totalPages": 25
  },
  "schema": {
    "name": "users",
    "columns": [...]
  }
}
```

### GET `/tables/{table_name}/export`
Returns exported data in CSV or JSON format.

## Project Structure

```
├── app/                    # Next.js app router
│   ├── page.tsx           # Main platform page
│   └── layout.tsx         # Root layout
├── components/            # React components
│   ├── Sidebar.tsx        # Table selection sidebar
│   ├── DataTable.tsx      # Data display table
│   ├── FilterPanel.tsx    # Filtering controls
│   ├── Pagination.tsx     # Pagination controls
│   └── TableHeader.tsx    # Table header info
├── hooks/                 # Custom React hooks
│   ├── useTableData.ts    # Data fetching hook
│   └── useTables.ts       # Tables list hook
├── lib/                   # Utilities
│   └── api.ts            # API client
└── types/                 # TypeScript definitions
    └── index.ts          # Shared types
```

## Technologies Used

- **Next.js 13**: React framework with App Router
- **TypeScript**: Type safety and better development experience
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Modern, accessible UI components
- **Lucide React**: Beautiful, customizable icons

## Deployment

The platform is configured for static export and can be deployed to any static hosting service:

```bash
npm run build
```

This creates an optimized production build in the `out` directory.