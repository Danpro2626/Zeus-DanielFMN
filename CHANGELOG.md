# Cambios

## 4.0.0
- **Nueva identidad visual:** logo (medidor de carga + rayo en Z), paleta medianoche/menta/cian y tipografías Sora y DM Sans.
- **Alertas sin bloqueo:** se eliminó la restricción del 20 %. Ya es posible ajustar la batería a cualquier valor (0–100), registrar recorridos que dejen la carga por debajo del límite y configurar el propio límite de alerta. Al llegar al límite o bajar de él se muestra un aviso (banner, color, notificación en pantalla y vibración).
- **Límites editables:** alerta y aviso de batería baja, capacidad, autonomía, peso y presión desde *Editar especificaciones*.
- **Se eliminó** toda referencia a terreno, clima, CO₂ ahorrado y eficiencia.
- **Importar respaldos** JSON (compatibles con exportaciones anteriores).
- El filtro del historial se genera con los meses que existen en los datos (antes estaba fijo hasta mayo de 2026).
- Sin dependencias externas: fuentes e iconos incluidos, funciona sin conexión.
- Iconos para PWA y recursos de icono para Android (adaptive icon, monocromático para iconos temáticos y PNG por densidad).
- Corregido: un nivel de batería de 0 % se restauraba a 100 % al recargar.
- Los datos guardados por la versión anterior se conservan (mismas claves de `localStorage`).
