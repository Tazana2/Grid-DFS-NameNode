# GridDFS - NameNode

El **NameNode** es el nodo maestro del sistema GridDFS.  
Su rol principal es **gestionar la metadata** de usuarios, directorios, archivos y bloques distribuidos en los DataNodes.

---

## 🚀 Funcionalidades principales
- Registro de DataNodes (manual y vía heartbeat).
- Manejo de directorios (`mkdir`, `rmdir`).
- Manejo de archivos (`put`, `get`, `rm`).
- Persistencia de metadata en `namenode_metadata.json`.
- Gestión multiusuario con autenticación básica.

---

## 🏗 Arquitectura de la API

- **Autenticación (`/auth`)**
  - `POST /auth/register` → Registro de usuario.
  - `POST /auth/login` → Inicio de sesión, retorna token JWT básico.

- **Gestión de directorios y archivos (`/namenode`)**
  - `POST /namenode/mkdir` → Crear directorio.
  - `DELETE /namenode/rmdir` → Eliminar directorio (y todos los archivos dentro).
  - `POST /namenode/allocate` → Asignar bloques de un archivo a DataNodes.
  - `DELETE /namenode/rm/{filename}` → Eliminar archivo.
  - `GET /namenode/metadata/{filename}` → Obtener metadata de un archivo.
  - `GET /namenode/ls` → Listar directorios y archivos.
  - `POST /namenode/register_datanode` → Registrar o refrescar estado de un DataNode (heartbeat).

---

## ▶️ Ejecución
```bash
uvicorn main:app
```

Por defecto en `http://127.0.0.1:8000/api/v1`.
