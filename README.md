# ISW2_DFARFAN
Relecloud Extended – Proyecto de Ingeniería del Software II
Relecloud Extended es la versión ampliada y colaborativa del proyecto individual desarrollado en la primera parte del curso. Su propósito es aplicar prácticas profesionales de ingeniería del software sobre una aplicación web construida con Django, integrando técnicas de desarrollo colaborativo, control de versiones, diseño orientado a features, trazabilidad, pruebas automáticas y despliegue continuo mediante Azure DevOps y Azure App Service.
La aplicación incorpora las mejoras funcionales definidas como Paquetes de Trabajo (PT1–PT4):
•	Envío real de correos electrónicos desde el formulario info_request.
•	Inclusión de imágenes propias en cada destino.
•	Sistema de reviews asociado a destinos y cruceros, disponible únicamente para usuarios que hayan realizado compras.
•	Cálculo y visualización de la valoración media, así como ordenación de destinos por popularidad.

Arquitectura del Proyecto
•	Lenguaje: Python 3.x
•	Framework: Django
•	Base de datos: PostgreSQL
•	Despliegue: Azure App Service
•	CI/CD: Azure DevOps Pipelines (YAML)
•	Control de versiones: Git con estrategia basada en ramas por feature
•	Pruebas: Django Test Framework (TDD aplicado en PT1 y PT3)

Paquetes de Trabajo (PT1–PT4)
PT	Descripción	
PT1	Envío de correo real desde info_request	
PT2	Imagen propia por destino	
PT3	Sistema de reviews + valoración media	
PT4	Ordenación por popularidad	
Cada PT se desarrolla en su propia rama y se integra mediante Pull Request revisado.

Backlog: Features, PBIs y Tareas
El backlog sigue una estructura jerárquica en Azure DevOps:
Features (nivel alto)
•	Gestión de solicitudes de información (PT1)
•	Gestión multimedia de destinos (PT2)
•	Sistema de reviews y valoración (PT3)
•	Destinos ordenados por popularidad (PT4)
PBIs
Cada Feature se descompone en PBIs que describen comportamientos observables desde la perspectiva del usuario.
Tareas
Cada PBI se descompone en tareas técnicas implementables (1 día aprox.).

Pruebas y TDD
•	PT1 y PT3 aplican Test-Driven Development.
•	Todos los PTs incluyen pruebas unitarias y funcionales.
•	El pipeline CI ejecuta automáticamente los test antes de permitir el merge a main.

Criterios de Aceptación (QAS)
Todos los PBIs incluyen criterios de aceptación descritos mediante Quality Attribute Scenarios, siguiendo el formato:
Agente – Estímulo – Artefacto – Condiciones – Respuesta – Métrica
Ejemplo (PT3 – Reviews):
Usuario autenticado que compró un destino (agente) intenta publicar una review (estímulo) sobre un destino (artefacto) habiendo completado el formulario correctamente (condición); la aplicación guarda la review y actualiza la media (respuesta) con un tiempo de proceso inferior a 150 ms (métrica).

Definition of Done (DoD)
Un PBI se considera completado cuando:
•	Se han definido y verificado los criterios QAS.
•	Incluye pruebas unitarias y/o funcionales.
•	El pipeline CI pasa sin errores.
•	La documentación del cambio está actualizada.
•	El PR ha sido revisado y aprobado por otro miembro del equipo.
•	El cambio está desplegado correctamente en Azure App Service.

Estrategia de Ramas y PRs
•	main: rama estable y protegida.
•	feature/PTx-nombre: una rama por Paquete de Trabajo.
•	Cada cambio se integra mediante Pull Request que debe incluir:
o	Relación con PBIs.
o	Evidencias del cumplimiento de la DoD.
o	Conversación y revisión entre miembros del equipo.
o	Validación automática por CI.

CI/CD – Pipeline en Azure DevOps
El archivo azure-pipelines.yml automatiza:
1.	Instalación del entorno.
2.	Instalación de dependencias.
3.	Ejecución de pruebas.
4.	Generación del paquete de despliegue.
5.	Publicación del artefacto.
6.	Despliegue automático en Azure App Service.

Despliegue en Azure
El entorno de producción en Azure App Service utiliza:
•	Configuración de variables de entorno (SECRET_KEY, EMAIL, DB, etc.)
•	Migraciones automáticas
•	Gestión de archivos estáticos
•	Integración con SendGrid para correo (PT1)

Contacto y Contribución
Este repositorio forma parte del proyecto colaborativo de Ingeniería del Software II.
Todos los miembros del equipo pueden contribuir según el flujo definido de ramas y PRs.

