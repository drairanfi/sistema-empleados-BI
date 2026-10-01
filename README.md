# Sistema de Empleados

Aplicación de escritorio en Python (Tkinter) que lee un archivo Excel de empleados, lo valida y permite consultarlo mediante botones.

## Requisitos

- Python 3.10 o superior, con Tkinter (incluido en el instalador oficial de Windows y macOS).
- `openpyxl`

## Instalación

Se recomienda usar un entorno virtual. En macOS con Python de Homebrew es obligatorio: instalar paquetes globalmente falla con el error `externally-managed-environment` (PEP 668).

### macOS / Linux

```bash
# Solo macOS con Homebrew: instalar soporte de Tkinter (ajuste la versión a su Python)
brew install python-tk@3.14

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

> Si el comando `pip` no existe, use siempre `python -m pip` (o `python3 -m pip`): ejecuta el pip del intérprete activo.

## Ejecución

Con el entorno virtual activado:

```bash
python main.py
```

1. Presione **Leer archivo Excel** y seleccione el archivo.
2. Si el archivo es válido, se habilitan las demás opciones.
3. Los listados se muestran en la tabla; los totales, en un cuadro de diálogo.

## Formato del archivo Excel

La primera hoja debe tener exactamente estas tres columnas, con encabezado en la fila 1:

| TIPODOC | NRODOCUMENTO | SUELDO |
|---------|--------------|--------|
| CC      | 1076669247   | 10000  |
| PAS     | 74320814     | 7000000 |

El archivo `empleados.xlsx` incluido en el proyecto es un ejemplo válido para probar la aplicación.

### Validaciones

| Validación | Ejemplo de mensaje |
|---|---|
| El archivo existe | `No se encontró el archivo: ...` |
| Extensión `.xlsx` / `.xlsm` | `Extensión '.csv' no válida...` |
| Archivo no vacío (0 bytes) | `El archivo está vacío (0 bytes).` |
| La hoja tiene datos | `La hoja no tiene datos.` |
| Hay empleados además del encabezado | `El archivo solo tiene encabezados, sin empleados.` |
| Número de columnas | `Se esperaban 3 columnas y se encontraron 2.` |
| Nombres de columnas | `Encabezados no válidos [...]` |
| TIPODOC no vacío y permitido | `Fila 3: TIPODOC 'XX' no es válido.` |
| NRODOCUMENTO no vacío y alfanumérico | `Fila 4: NRODOCUMENTO está vacío.` |
| SUELDO numérico y no negativo | `Fila 5: SUELDO 'abc' no es numérico.` |
| Sin datos fuera de las 3 columnas | `Fila 6: tiene datos fuera de las columnas esperadas.` |

Se reportan todos los errores a la vez, con el número de fila real de Excel. Las filas completamente vacías se ignoran.

Los tipos de documento permitidos (`CC`, `CE`, `PAS`, `TI`, `NIT`) se configuran en `config.py`.

## Opciones del menú

| Botón | Función en `employee_service.py` | Comportamiento |
|---|---|---|
| Mostrar empleados | `list_employees` | Lista todos los empleados |
| Buscar empleado | `search_employee` | Busca por número de documento; muestra todas las coincidencias (un número puede repetirse con distinto tipo de documento) |
| Total de sueldos | `total_salaries` | Suma de todos los sueldos |
| Sueldo promedio | `average_salary` | Promedio de sueldos |
| Empleado con mayor sueldo | `highest_paid_employees` | Muestra el o los empleados con el sueldo más alto (incluye empates) |
| Empleados por sueldo | `employees_by_salary` | Filtra por rango mínimo/máximo (ambos opcionales) y ordena de mayor a menor |
| Salir | — | Cierra la aplicación |

## Estructura

Cada archivo tiene una única responsabilidad:

```
sistema_empleados/
├── main.py              # Punto de entrada
├── gui.py               # Interfaz Tkinter (solo presentación y entrada del usuario)
├── employee_service.py  # Lógica de negocio: una función por opción del menú
├── excel_reader.py      # Convierte las filas validadas en objetos Employee
├── excel_validator.py   # Validación del archivo y su contenido
├── employee.py          # Modelo de datos Employee
├── config.py            # Constantes (columnas, tipos de documento, extensiones)
└── requirements.txt
```

Flujo de dependencias:

```
main → gui → excel_reader → excel_validator → config
         └─→ employee_service        └─→ employee
```

La lógica (`employee_service`, `excel_validator`) no depende de Tkinter, por lo que puede reutilizarse desde consola, pruebas o una aplicación web reemplazando solo `gui.py`.
