# Sistema de Gestión de Licitaciones

Aplicación backend desarrollada con Django REST Framework para la gestión de clientes, productos y licitaciones con control de presupuesto y auditoría de usuarios.

---

## Autenticación

Se utiliza JWT para autenticación.

### Login:

POST `/api/token/`

```json
{
  "email": "prueba_1@gmail.com",
  "password": "prueba_1234"
}
```

---

## Funcionalidades

### Usuarios

* Login con email
* Roles: admin / user
* Admin puede crear usuarios

### Clientes

* CRUD completo
* Auditoría (created_by, updated_by)

### Productos

* CRUD completo
* Validación de precio > 0

### Licitaciones

* CRUD completo
* Asociadas a clientes
* Presupuesto máximo validado
* Cálculo automático de total

### Licitación - Productos

* Agregar productos a licitación
* Validación de cantidad > 0
* No exceder presupuesto

---

## Reglas de negocio

* No se permiten valores negativos
* No se puede exceder el presupuesto
* Auditoría automática por usuario autenticado

---

## Frontend básico

* Login
* Dashboard
* Listado de clientes, productos y licitaciones

---

## Tecnologías

* Django
* Django REST Framework
* JWT (SimpleJWT)
* PostgreSQL
* Render (deploy)

---

## Deploy

https://licitaciones-api-xgh2.onrender.com

---

## Autor Miguel Mark

Proyecto desarrollado como prueba técnica.
