# neo4jtest

This example demonstrates how to use the official `neo4j` Python driver to load a
simple dependency graph of modules and functions.

## Requirements

- Python 3.8+
- `neo4j` Python package
- A running Neo4j instance accessible via Bolt (e.g. `bolt://localhost:7687`)

Install the driver with:

```bash
pip install neo4j
```

Set the connection details via environment variables if needed:

```bash
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=test
```

## Running

Execute the script to reset the database, create nodes and relationships, and
query nodes connected to module `A`:

```bash
python test_neo4j.py
```

The output will list the nodes connected to module A.
