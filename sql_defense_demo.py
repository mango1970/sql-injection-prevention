#!/usr/bin/env python3
"""
Script: sql_defense_demo.py
Descripción: Demostración interactiva de una vulnerabilidad SQL Injection (SQLi)
             y su mitigación mediante el uso de Consultas Preparadas.
Autor: Mauricio Núñez G.
"""

import sqlite3
import os

# 1. Inicializar una base de datos en memoria para el laboratorio
def inicializar_base_de_datos():
    conexion = sqlite3.connect(":memory:") # Base de datos temporal y segura
    cursor = conexion.cursor()
    
    # Crear tabla de usuarios simulada
    cursor.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cuenta TEXT,
            contrasena TEXT,
            rol TEXT
        )
    """)
    
    # Insertar datos de prueba (Simulando un entorno real)
    usuarios_demo = [
        ('admin', 'SuperSecretPassword2026', 'Administrador'),
        ('mauro', 'BeeKeeperSecure99!', 'Consultor'),
        ('carlos', 'LinuxUserPass456', 'Desarrollador')
    ]
    cursor.executemany("INSERT INTO usuarios (cuenta, contrasena, rol) VALUES (?, ?, ?)", usuarios_demo)
    conexion.commit()
    return conexion

# 2. ENFOQUE VULNERABLE: Concatenación directa de strings
def login_vulnerable(conexion, usuario_input, password_input):
    cursor = conexion.cursor()
    
    # MALAS PRÁCTICAS: Al usar f-strings o concatenar con '+', la entrada se vuelve parte del comando ejecutable
    query = f"SELECT cuenta, rol FROM usuarios WHERE cuenta = '{usuario_input}' AND contrasena = '{password_input}'"
    
    print(f"\n[DEBUG] Consulta SQL ejecutada (Vulnerable):\n  {query}")
    
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        return f"Error en la base de datos: {e}"

# 3. ENFOQUE SEGURO: Consultas Parametrizadas (Security by Design)
def login_seguro(conexion, usuario_input, password_input):
    cursor = conexion.cursor()
    
    # BUENAS PRÁCTICAS: Los marcadores '?' le dicen al motor SQL que trate la entrada estrictamente como datos, nunca como código
    query = "SELECT cuenta, rol FROM usuarios WHERE cuenta = ? AND contrasena = ?"
    
    print(f"\n[DEBUG] Consulta SQL ejecutada (Segura/Parametrizada):\n  {query} | Parámetros: ('{usuario_input}', '{password_input}')")
    
    cursor.execute(query, (usuario_input, password_input))
    return cursor.fetchall()

# --- FLUJO PRINCIPAL DEL LABORATORIO ---
if __name__ == "__main__":
    db = inicializar_base_de_datos()
    
    print("=" * 70)
    print("   LABORATORIO DE CIBERSEGURIDAD: MITIGACIÓN DE SQL INJECTION (SQLi)   ")
    print("=" * 70)
    
    # --- ESCENARIO 1: Intento de ataque en la función vulnerable ---
    print("\n--- ESCENARIO 1: Ataque de evasión de autenticación en login vulnerable ---")
    
    # El atacante inyecta una compuerta lógica OR que siempre es verdadera ('1'='1) y comenta el resto (--)
    ataque_usuario = "admin' OR '1'='1"
    ataque_password = "lo que sea"
    
    resultado_vulnerable = login_vulnerable(db, ataque_usuario, ataque_password)
    
    print("\n[RESULTADO] Respuesta del sistema vulnerable:")
    if resultado_vulnerable:
        print(f"  ❌ ¡Acceso Concedido de forma ilícita! Datos expuestos: {resultado_vulnerable}")
    else:
        print("  Acceso denegado.")
        
    # --- ESCENARIO 2: El mismo ataque frente a la función mitigada ---
    print("\n" + "-" * 70)
    print("--- ESCENARIO 2: Mismo ataque frente a función con Diseño Seguro ---")
    
    resultado_seguro = login_seguro(db, ataque_usuario, ataque_password)
    
    print("\n[RESULTADO] Respuesta del sistema seguro:")
    if resultado_seguro:
        print(f"  Acceso Concedido: {resultado_seguro}")
    else:
        print("  ✅ ¡Acceso Denegado! El sistema neutralizó la inyección y buscó literalmente el usuario 'admin' OR '1'='1'.")
        
    print("=" * 70)
    db.close()