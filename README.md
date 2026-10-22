# Sprint 1 - Proyecto RII 3: Robots Inteligentes

## Grupo 10

Este repositorio contiene el workspace de ROS 2 del grupo 10 para el Sprint 1 del proyecto RII 3.

### Requisitos

- Ubuntu con ROS 2 Jazzy
- Python 3
- `colcon`

## Descargar el proyecto

Clonar el repositorio:

```bash
git clone https://github.com/jorge3x0-sys/Sprint1.git
```

Entrar en el workspace:

```bash
cd Sprint1
```

## Compilar

Cargar ROS 2 Jazzy:

```bash
source /opt/ros/jazzy/setup.bash
```

Compilar el workspace:

```bash
colcon build
```

Cargar el workspace compilado:

```bash
source install/setup.bash
```

## Ejecutar

Ejecutar el launch del proyecto:

```bash
ros2 launch g10_prii3_turtlesim turtle.launch.py
```

El proyecto abre `turtlesim` y ejecuta el nodo de control de la tortuga.

## Estructura del proyecto

```text
.
└── g10_prii3_turtlesim
    ├── g10_prii3_turtlesim
    │   ├── __init__.py
    │   └── turtle_controller.py
    ├── launch
    │   └── turtle.launch.py
    ├── package.xml
    ├── resource
    │   └── g10_prii3_turtlesim
    ├── setup.cfg
    ├── setup.py
    └── test
        ├── test_copyright.py
        ├── test_flake8.py
        └── test_pep257.py

```

## Git

La rama principal del proyecto es:

```text
main
```

Repositorio:

https://github.com/jorge3x0-sys/Sprint1
