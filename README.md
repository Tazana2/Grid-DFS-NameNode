# Grid-DFS

A minimal distributed file system (DFS) that stores files split into blocks across multiple DataNodes and keeps metadata in a NameNode.


## Features (MVP)

* NameNode service (FastAPI): manages metadata, DataNode registry and block allocation.
* DataNode service (FastAPI): accepts block uploads, serves block downloads, reports health.
* CLI client (`gridfs`): `put`, `get`, `ls`, `rm`, `mkdir`, `rmdir` (minimal UX).
* Simple round-robin block allocation and configurable block size (default 64 MB).
* Docker Compose to launch 1 NameNode + 3 DataNodes for demo/testing.


## Architecture and API

### NameNode

* `POST /auth/login` — simple auth (returns token)
* `POST /namenode/register_datanode` — register a DataNode (called at DataNode startup)
* `POST /namenode/allocate` — request block allocation for a file (returns block list with target DataNodes)
* `GET  /namenode/metadata/{filename}` — retrieve metadata for a file

> NameNode stores metadata in a lightweight on-disk store (JSON or SQLite) suitable for the assignment.

### DataNode

* `POST /datanode/register` — register with NameNode on startup
* `PUT  /datanode/block/{block_id}` — upload a block (binary)
* `GET  /datanode/block/{block_id}` — download a block
* `GET  /datanode/health` — health check and basic stats


## CLI (client)

Basic commands provided by `client/cli.py`:

* `put <file>` — split file to blocks, request allocation and upload blocks to DataNodes.
* `get <file>` — retrieve blocks from DataNodes and reconstruct the file.
* `ls` — list files known to the NameNode.
* `rm <file>` — delete file metadata and request DataNodes to delete blocks.
* `mkdir` / `rmdir` — optional directory emulation (simple implementation)

Usage examples:

```bash
python3 client/cli.py put sample.bin
python3 client/cli.py ls
python3 client/cli.py get sample.bin
```

## Configuration

* `BLOCK_SIZE` (default 64 MB) — configurable in client and NameNode allocation calls.
* Ports and addresses are configured via environment variables or `docker-compose.yml`.
* Persistence for NameNode metadata can be a JSON file or SQLite DB (configurable in the NameNode code).

## Known limitations and future improvements

* No replication implemented (MVP). Add replication for fault tolerance.
* No sophisticated failure recovery (e.g., re-replication of lost blocks).
* Authentication is intentionally simple.
* Performance optimizations: parallel uploads/downloads, chunked streaming, back-pressure handling.