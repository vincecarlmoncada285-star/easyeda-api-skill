# UNIQUE-CANE circuit schematic

Schematic for Figure 2 of *UNIQUE-CANE: An Enhanced White Cane with Ultrasonic
Obstacle Detection for The Visually Impaired*. It follows Table 1 (ESP32 WROOM32 Pin Assignments) of the paper.

- `unique_cane_schematic.png`: 300 dpi image for the paper
- `unique_cane_schematic.svg`: vector version
- `unique_cane_schematic.py`: source (`pip install schemdraw matplotlib && python unique_cane_schematic.py`)

## Netlist

| Net  | Connections |
|------|-------------|
| VBAT+ | BT1 + → SW1 → U4 VIN+ |
| +5V  | U4 VOUT+, U1 5V, U3 VM |
| 3V3  | U1 3V3, U2 VCC, U3 VCC, U3 STBY, U3 PWMA |
| GND  | BT1 −, U4 VIN− / VOUT−, U1 GND, U2 GND, U3 GND |
| TRIG | U1 GPIO5 (D5) → U2 TRIG |
| ECHO | U2 ECHO → U1 GPIO18 (D18) |
| IN1  | U1 GPIO19 (D19) → U3 AIN1 |
| IN2  | U1 GPIO21 (D21) → U3 AIN2 |
| MOT+ / MOT− | U3 AO1 / AO2 → M1 |
