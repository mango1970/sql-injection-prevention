🔍 El Problema: Consultas Dinámicas Inseguras
Cuando una aplicación concatena directamente la entrada del usuario dentro de una consulta SQL, permite que un atacante inyecte comandos maliciosos. Esto puede resultar en la evasión de autenticación, fuga de información confidencial o destrucción de la base de datos.

Ejemplo de Código Vulnerable (Concatenación Directa):
SELECT * FROM usuarios WHERE cuenta = 'INPUT_USUARIO' AND contrasena = 'INPUT_PASSWORD';
Si el usuario ingresa: admin' OR '1'='1
El resultado es que el atacante elude por completo la autenticación.

🛡️ La Solución: Consultas Preparadas (Parametrización)
La mitigación definitiva consiste en separar estrictamente el código de los datos. Al utilizar consultas preparadas (Prepared Statements), el motor de la base de datos compila la estructura de la consulta primero y trata la entrada del usuario estrictamente como un valor literal, neutralizando cualquier intento de inyección.

Ejemplo de Mitigación (Estructura Segura):
SELECT * FROM usuarios WHERE cuenta = ? AND contrasena = ?;
Los marcadores de posición (?) aseguran que la entrada jamás se ejecute como un comando.

🧪 El Laboratorio Práctico (sql_defense_demo.py)
Este repositorio incluye un script interactivo en Python que simula un sistema de autenticación utilizando una base de datos SQLite en memoria (:memory:). El script recrea un ataque de bypass de login en un entorno vulnerable y demuestra cómo el mismo ataque falla al aplicar diseño seguro.

Cómo ejecutar el laboratorio:

Asegúrate de tener Python 3 instalado.

Ejecuta el script desde tu terminal: python3 sql_defense_demo.py

📈 Valor Técnico del Proyecto
Sanitización de Entradas: Demostración de principios de validación y tipado estricto de datos.

Defensa en Capas: Aplicación del principio de mínimo privilegio en las cuentas de conexión a la base de datos.

🇺🇸 English Version
🔍 The Problem: Insecure Dynamic Queries
When an application directly concatenates user input into a SQL query, it allows an attacker to inject malicious commands. This can lead to authentication bypass, data exfiltration, or complete database destruction.

Vulnerable Code Example (Direct Concatenation):
SELECT * FROM users WHERE account = 'USER_INPUT' AND password = 'PASSWORD_INPUT';
If the user inputs: admin' OR '1'='1
The result is that the attacker completely bypasses authentication.

🛡️ The Solution: Prepared Statements (Parametrization)
The definitive mitigation is to strictly separate code from data. By using prepared statements, the database engine compiles the query structure first and treats the user input strictly as a literal value, neutralizing any injection attempt.

Mitigation Example (Secure Structure):
SELECT * FROM users WHERE account = ? AND password = ?;
Placeholders (?) ensure that the input is never executed as a command.

🧪 The Practical Lab (sql_defense_demo.py)
This repository features an interactive Python script simulating an authentication system with an in-memory SQLite database (:memory:). The script recreates a login bypass attack within a vulnerable setup and demonstrates how the very same exploit fails under a Secure by Design architecture.

How to run the lab:

Ensure you have Python 3 installed.

Run the script from your terminal: python3 sql_defense_demo.py

📈 Technical Value of this Project
Input Sanitization: Demonstrates principles of data validation and data typing.

Defense in Depth: Implementation of the principle of least privilege for database connection accounts.

📄 Licencia / License
Este proyecto está bajo la Licencia MIT / This project is licensed under the MIT License.