# 🌍 Traductor Alemán ↔ Español

Aplicación sencilla de traducción desarrollada con un modelo local de IA (**Qwen2-0.5B-Instruct**), sin uso de APIs externas.

---

## 🚀 Descripción

Este proyecto consiste en una pequeña app que permite traducir texto entre **alemán y español** utilizando un modelo de lenguaje ejecutado de forma local.

La interfaz está hecha en HTML y se conecta a un servidor en Python que realiza las traducciones.

---

## 🧠 Tecnologías utilizadas

* Python
* Flask
* Transformers (Hugging Face)
* PyTorch
* HTML

---

## ⚙️ Cómo ejecutar el proyecto

1. Instalar dependencias:

```bash
pip install flask flask-cors transformers torch
```

2. Ejecutar el servidor:

```bash
python translator_server.py
```

3. Abrir el archivo en tu navegador:

```bash
index.html
```

---

## 📸 Screenshot

![App](screenshot.png)

---

## 🌐 Versión en línea

Puedes ver la interfaz en GitHub Pages:

👉 https://alexglezcontreras-maker.github.io/4_mayo/

> ⚠️ Nota: GitHub Pages solo permite contenido estático, por lo que la traducción no funciona en línea.
> Para usar la funcionalidad completa, es necesario correr el servidor localmente.

---

## ✅ Ejemplos de uso

* I like soccer → Me gusta el fútbol
* How are you? → ¿Cómo estás?
* What time is it? → ¿Qué hora es?

---

## 👤 Autor

Proyecto desarrollado por Alex González.
