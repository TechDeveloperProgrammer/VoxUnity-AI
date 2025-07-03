# Política de Seguridad de VoxUnity AI+

La seguridad es una prioridad fundamental para VoxUnity AI+. Nos comprometemos a proteger la privacidad y la integridad de los datos de nuestros usuarios, así como a mantener la robustez de nuestra plataforma. Agradecemos a la comunidad de seguridad por su ayuda en la identificación y divulgación responsable de vulnerabilidades.

## Cómo Reportar una Vulnerabilidad

Si descubres una vulnerabilidad de seguridad en VoxUnity AI+, te pedimos que la reportes de manera responsable y privada. **Por favor, NO abras un issue público en GitHub para reportar vulnerabilidades de seguridad.**

Envía un correo electrónico detallado a [EMAIL DE SEGURIDAD] (ej. `security@voxunity.ai` o un alias de equipo).

En tu reporte, por favor, incluye la siguiente información:

*   **Descripción:** Una descripción clara y concisa de la vulnerabilidad.
*   **Pasos para Reproducir:** Instrucciones detalladas y reproducibles para que podamos verificar la vulnerabilidad. Incluye código, configuraciones, capturas de pantalla o videos si es posible.
*   **Impacto Potencial:** Explica el impacto potencial de la vulnerabilidad (ej. robo de datos, ejecución remota de código, denegación de servicio).
*   **Versiones Afectadas:** Las versiones de VoxUnity AI+ que crees que están afectadas.
*   **Tu Contacto:** Tu nombre (opcional) y cómo podemos contactarte para más detalles o para informarte sobre el progreso.

Nos comprometemos a:

*   Acusar recibo de tu reporte en un plazo de 24-48 horas hábiles.
*   Investigar a fondo la vulnerabilidad.
*   Mantenerte informado sobre el progreso de la investigación y la resolución.
*   Reconocer públicamente tu contribución (si lo deseas) una vez que la vulnerabilidad haya sido mitigada.

## Prácticas de Desarrollo Seguro

Nuestro equipo sigue las siguientes prácticas para garantizar la seguridad del código:

*   **Validación de Entradas:** Todas las entradas de usuario son validadas y sanitizadas para prevenir ataques como inyección SQL, XSS, etc.
*   **Cifrado de Datos Sensibles:** Los datos sensibles (ej. entradas del diario de terapia) se cifran en reposo utilizando algoritmos robustos (Fernet/AES).
*   **Gestión de Secretos:** Las claves API, credenciales y otros secretos se gestionan a través de variables de entorno y no se hardcodean en el código fuente.
*   **Hashing de Contraseñas:** Las contraseñas de usuario se almacenan utilizando funciones de hashing seguras (ej. bcrypt) con salts adecuados.
*   **Principios de Mínimo Privilegio:** Los componentes y usuarios operan con los permisos mínimos necesarios para realizar sus funciones.
*   **Análisis de Seguridad Estático (SAST):** Utilizamos herramientas como `Bandit` en nuestro CI/CD para identificar vulnerabilidades comunes en el código Python.
*   **Actualizaciones de Dependencias:** Mantenemos nuestras dependencias actualizadas para mitigar vulnerabilidades conocidas en librerías de terceros.
*   **Revisión de Código:** Todos los cambios de código son revisados por al menos un miembro del equipo antes de ser fusionados.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.