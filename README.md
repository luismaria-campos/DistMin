# Algoritmo de programación para la optimización de batería

**Autor:** Luis María Campos de la Morena  
**Email:** [luismaria.Camposm@gmail.com](mailto:luismaria.Camposm@gmail.com)  

## Descripción

`dist_min.py` implementa un **algoritmo de programación de tareas** que:

- Asigna tareas a ranuras horarias según energía disponible y QoS.  
- Minimiza la diferencia de la batería respecto al valor inicial.  
- Mantiene la batería dentro de los límites `B_MIN` y `B_MAX`.  
- Muestra resultados y gráficos de **batería** y **QoS**.

## Requisitos

- Python 3  
- Matplotlib:  

```bash
pip install matplotlib
```

## Uso

Ejecuta el script:

```bash
python3 dist_min.py
```