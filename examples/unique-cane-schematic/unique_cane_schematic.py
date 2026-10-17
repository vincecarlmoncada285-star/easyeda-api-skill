"""Circuit schematic for the UNIQUE-CANE prototype (Figure 2 of the paper).

Board: classic ESP32-DevKitC (ESP32-WROOM-32). Pin map: TRIG = GPIO18,
ECHO = GPIO19, PWMA = GPIO21, AIN2 = GPIO22. Run:

    pip install schemdraw matplotlib
    python unique_cane_schematic.py

Outputs unique_cane_schematic.png (300 dpi) and unique_cane_schematic.svg.
"""

import os

import schemdraw
import schemdraw.elements as elm

HERE = os.path.dirname(os.path.abspath(__file__))

schemdraw.config(fontsize=11, font='DejaVu Sans', lw=1.4)


def P(name, side, slot=None):
    return elm.IcPin(name=name, side=side, slot=slot)


def wire(d, *pts):
    """Draw an orthogonal wire through the given points."""
    for a, b in zip(pts, pts[1:]):
        d += elm.Line().endpoints(a, b)


def vdd(d, at, label, rise=0.7):
    top = (at[0], at[1] + rise)
    wire(d, at, top)
    d += elm.Vdd().at(top).theta(0).label(label, fontsize=10)


def gnd(d, at, drop=0.7):
    bot = (at[0], at[1] - drop)
    wire(d, at, bot)
    d += elm.Ground().at(bot).theta(0)


def siglabel(d, at, text):
    d += elm.Label().at((at[0] + 0.25, at[1] + 0.22)).label(text, fontsize=9, halign='left', color='#444444')


with schemdraw.Drawing(show=False) as d:

    # ---------------- U1 ESP32-DevKitC (centre) ----------------
    esp = elm.Ic(
        pins=[P('5V', 'top'), P('3V3', 'top'),
              P('GND', 'bot'),
              P('GPIO22', 'right'), P('GPIO21', 'right'),
              P('GPIO19', 'right'), P('GPIO18', 'right')],
        size=(4.6, 7.0), pinspacing=1.4, leadlen=0.7, plblsize=10,
    ).theta(0).at((0, 0)).anchor('center').label('U1\nESP32-DevKitC\n(ESP32-WROOM-32)', 'center', fontsize=12, ofst=(-0.45, 0.35))
    d += esp

    # ---------------- U2 HC-SR04 (top right) ----------------
    us = elm.Ic(
        pins=[P('VCC', 'top'), P('GND', 'bot'),
              P('ECHO', 'left'), P('TRIG', 'left')],
        size=(4.6, 3.4), pinspacing=1.2, leadlen=0.7, plblsize=10,
    ).theta(0).at((12.5, 5.6)).anchor('center').label('U2\nHC-SR04\nUltrasonic\nSensor', 'center', fontsize=11, ofst=(0.35, 0))
    d += us

    # ---------------- U3 TB6612FNG (bottom right) ----------------
    drv = elm.Ic(
        pins=[P('VCC', 'top'), P('STBY', 'top'), P('AIN1', 'top'), P('VM', 'top'),
              P('GND', 'bot'),
              P('AIN2', 'left', '2/5'), P('PWMA', 'left', '4/5'),
              P('AO2', 'right', '2/5'), P('AO1', 'right', '4/5')],
        size=(5.2, 4.4), pinspacing=1.3, leadlen=0.7, plblsize=10,
    ).theta(0).at((12.5, -5.4)).anchor('center').label('U3\nTB6612FNG\nMotor Driver (ch. A)', 'center', fontsize=11)
    d += drv

    # ---------------- U4 DC-DC boost converter (left) ----------------
    boost = elm.Ic(
        pins=[P('VIN−', 'left'), P('VIN+', 'left'),
              P('VOUT−', 'right'), P('VOUT+', 'right')],
        size=(4.8, 3.6), pinspacing=1.8, leadlen=0.7, plblsize=10,
    ).theta(0).at((-9.0, 1.2)).anchor('center').label('U4\nDC-DC Boost\nConverter\n(5.0 V out)', 'center', fontsize=10)
    d += boost

    # ---- ESP32 -> HC-SR04 signals (TRIG = GPIO18, ECHO = GPIO19) ----
    x_trig, x_echo = 6.4, 7.6
    t, e = esp.GPIO18, esp.GPIO19
    wire(d, t, (x_trig, t[1]), (x_trig, us.TRIG[1]), us.TRIG)
    wire(d, e, (x_echo, e[1]), (x_echo, us.ECHO[1]), us.ECHO)
    siglabel(d, t, 'TRIG')
    siglabel(d, e, 'ECHO')

    # ---- ESP32 -> TB6612FNG control (PWMA = GPIO21, AIN2 = GPIO22) ----
    x_dir, x_pwm = 6.4, 7.6
    p, r = esp.GPIO21, esp.GPIO22
    wire(d, p, (x_pwm, p[1]), (x_pwm, drv.PWMA[1]), drv.PWMA)
    wire(d, r, (x_dir, r[1]), (x_dir, drv.AIN2[1]), drv.AIN2)
    siglabel(d, p, 'PWM')
    siglabel(d, r, 'DIR')

    # ---- HC-SR04 power ----
    vdd(d, us.VCC, '+5V')
    gnd(d, us.GND)

    # ---- TB6612FNG power and tie-highs: VCC, STBY, AIN1 -> 3V3 ; VM -> +5V ----
    y_bus = drv.VCC[1] + 0.7
    for name in ('VCC', 'STBY', 'AIN1'):
        wire(d, drv[name], (drv[name][0], y_bus))
    wire(d, (drv.VCC[0], y_bus), (drv.AIN1[0], y_bus))
    d += elm.Dot().at((drv.STBY[0], y_bus))
    mid = ((drv.VCC[0] + drv.STBY[0]) / 2, y_bus)
    vdd(d, mid, '3V3', rise=0.5)
    vdd(d, drv.VM, '+5V')
    gnd(d, drv.GND)

    # ---- Vibration motor on AO1 (+) / AO2 (−) ----
    x_m = drv.AO1[0] + 1.6
    wire(d, drv.AO1, (x_m, drv.AO1[1]))
    wire(d, drv.AO2, (x_m, drv.AO2[1]))
    d += elm.Motor().endpoints((x_m, drv.AO1[1]), (x_m, drv.AO2[1])).label('M1\nVibration\nMotor', loc='bottom', ofst=0.3, fontsize=10)
    d += elm.Label().at((x_m - 0.55, drv.AO1[1] + 0.3)).label('+', fontsize=11)

    # ---- ESP32 power ----
    vdd(d, esp['3V3'], '3V3')
    gnd(d, esp.GND)

    # ---- +5V rail: boost VOUT+ -> ESP32 5V ----
    vo = boost['VOUT+']
    y_rail = esp['5V'][1] + 1.0
    x_tap = vo[0] + 1.4
    wire(d, vo, (x_tap, vo[1]), (x_tap, y_rail), (esp['5V'][0], y_rail), esp['5V'])
    d += elm.Dot().at((x_tap, y_rail))
    vdd(d, (x_tap, y_rail), '+5V', rise=0.6)
    wire(d, boost['VOUT−'], (x_tap, boost['VOUT−'][1]))
    gnd(d, (x_tap, boost['VOUT−'][1]))

    # ---- Battery pack -> SW1 -> VIN+ ; battery − -> VIN− ----
    vi_p, vi_n = boost['VIN+'], boost['VIN−']
    x_bat = vi_p[0] - 5.0
    sw_r = (vi_p[0] - 1.0, vi_p[1])
    sw_l = (vi_p[0] - 3.2, vi_p[1])
    wire(d, vi_p, sw_r)
    d += elm.Switch().endpoints(sw_r, sw_l).label('SW1\nRocker switch', loc='top', ofst=0.25, fontsize=10)
    y_bb = vi_n[1] - 2.2
    wire(d, sw_l, (x_bat, vi_p[1]), (x_bat, vi_p[1] - 0.6))
    d += elm.Battery().endpoints((x_bat, vi_p[1] - 0.6), (x_bat, y_bb + 1.0))
    d += elm.Label().at((x_bat - 0.6, (vi_p[1] + y_bb) / 2)).label(
        'BT1\n1S4P Li-ion pack\n4 × ICR18650\nin parallel\n3.7 V nom.\n(3.0–4.2 V)', fontsize=10, halign='right')
    x_n = vi_n[0] - 1.0
    wire(d, (x_bat, y_bb + 1.0), (x_bat, y_bb), (x_n, y_bb), (x_n, vi_n[1]), vi_n)
    d += elm.Label().at((x_bat + 0.4, vi_p[1] - 0.75)).label('+', fontsize=11)

    # ---- Notes ----
    d += elm.Label().at((-17.5, -9.4)).label(
        'Notes:  All ground symbols are one common ground.   +5V = boost converter VOUT+.   '
        '3V3 = ESP32-DevKitC on-board 3.3 V regulator output.\n'
        'TB6612FNG channel B (BIN1, BIN2, PWMB, BO1, BO2) is unused.',
        fontsize=9.5, halign='left', valign='top')

    d.save(os.path.join(HERE, 'unique_cane_schematic.svg'))
    d.save(os.path.join(HERE, 'unique_cane_schematic.png'), dpi=300)
