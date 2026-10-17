# UNIQUE-CANE circuit schematic

Schematic for Figure 2 of *UNIQUE-CANE: An Enhanced White Cane with Ultrasonic
Obstacle Detection for The Visually Impaired*. It is drawn from Table 1 of the paper and the researchers' Cirkit Designer wiring diagram,
with the controller changed to the classic ESP32-DevKitC (ESP32-WROOM-32).

The classic ESP32 has no GPIO20 or GPIO47, so the signal pins were remapped to
GPIO18, GPIO19, GPIO21 and GPIO22. None of these are strapping, flash or PSRAM pins.
Table 1 and the Arduino sketch must use the same pin numbers.

- `unique_cane_schematic.png`: 300 dpi image for the paper
- `unique_cane_schematic.svg`: vector version
- `unique_cane_schematic.py`: source (`pip install schemdraw matplotlib && python unique_cane_schematic.py`)

## Netlist

| Net  | Connections |
|------|-------------|
| VBAT+ | BT1 + → SW1 → U4 VIN+ |
| +5V  | U4 VOUT+, U1 5V, U2 VCC, U3 VM |
| 3V3  | U1 3V3, U3 VCC, U3 STBY, U3 AIN1 |
| GND  | BT1 −, U4 VIN− / VOUT−, U1 GND, U2 GND, U3 GND |
| TRIG | U1 GPIO18 → U2 TRIG |
| ECHO | U2 ECHO → U1 GPIO19 |
| PWM  | U1 GPIO21 → U3 PWMA |
| DIR  | U1 GPIO22 → U3 AIN2 |
| MOT+ / MOT− | U3 AO1 / AO2 → M1 |
