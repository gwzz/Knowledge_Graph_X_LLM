# Knowledge_Graph_X_LLM

Knowledge_Graph_X_LLM is a toolkit for generating, managing, and visualizing knowledge graphs (KG) using Large Language Models (LLMs). This project provides an end-to-end pipeline for extracting structured knowledge from unstructured text, managing the resulting knowledge graph, and visualizing it interactively.

## Features

- **Knowledge Graph Generation**: Automatically extract entities and relationships from text using LLMs.
- **Knowledge Graph Management**: Store, update, and query knowledge graphs efficiently.
- **Visualization**: Interactive visualization tools for exploring and analyzing the knowledge graph.
- **Service APIs**: Expose KG operations via RESTful APIs for integration with other applications.
- **Knowledge Server**: Centralized server for managing, querying, and serving knowledge graph data to clients and applications.

## Project Structure

```
Knowledge_Graph_X_LLM/
├── knowledge_graph_generator/      # KG extraction and LLM integration
├── knowledge_server/               # Centralized server for KG management and APIs
├── visulization/
│   └── graph-visualization/        # Next.js-based 3D visualization web app
├── data/                           # Example input/output data and KG files
├── docs/                           # Documentation and usage guides
├── LICENSE
├── .gitignore
├── README.md
```

