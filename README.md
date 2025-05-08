# CorroSenseBoardV4

This repository contains documentation, Altium design files, and software for the **CorroSenseBoardV4**.

## Jumpers on PCB

Several jumpers must be configured correctly for the board to function as intended. The jumpers are explained below, grouped by the board type.

---

### Motherboard

#### Power Source Configuration

- **P400 (Pin 2 ↔ Pin 3):**  
  Selects the power source as **internal (USB/BAT)** instead of **energy harvesting**.

- **P401 (Pin 1 ↔ Pin 2):**  
  Selects the **battery** as the power source instead of **USB**.

- **P402 (Pin 2 ↔ Pin 3):**  
  Selects the power source as **internal (USB/BAT)** instead of **energy harvesting**.

#### Signal Routing

- **P105 (Pin 1 ↔ Pin 2):**  
  Routes the **DDS signal** to **P104**, the PZT connector on the motherboard.

- **P106 (Pin 1 ↔ Pin 2):**  
  Sends the **PZT output** to the **TIA** on the motherboard.

- **P107:**  
  *(Function not yet documented)*

![Motherboard](figures/Motherboard.jpg)

---

The board can then be powered on J101 with max 5VDC and min 3VDC.

### Daughterboard

*(Add relevant jumper details here if available)*

## Issues and TODO

#### Motherboard

- The very first ADC reading is always maximum value, doing 1 reading before main loop (and not saving the data) solves the issue.

- Mag and phase measure measurements are identical.

- The DDS gain is highly frequency dependent, above 100kHz the sinewave becomes more like a saw and amplitude of signal decreases. This happens ... could be because of OPAMPS or digital pot.

- Calculate phase and mag, find the right formula, struggling to get correct results, could be due to the VCOMM of 1.4V instead of 0.

- A good measurement is highly dependent on TIA gain and frequency... how to automate it? Maybe make a measurement on the TIA over frequency..?





