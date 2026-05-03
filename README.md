# ❤️ HeartSync: Open-Source Pulse Monitoring

> *Democratizing health tracking with a high-precision, low-cost Arduino-based Photoplethysmography (PPG) system.*

## 🌟 Overview

Clinical-grade heart rate monitors offer high accuracy but are often cost-prohibitive, while affordable wearables can sometimes lack precision **HeartSync** bridges this gap by providing an accessible, portable, and highly reliable alternative for continuous heart rate monitoring. Utilizing transmissive PPG technology, HeartSync detects pulsatile blood flow through skin light absorption and processes the data locally to deliver real-time Beats Per Minute (BPM) 

## ✨ Key Features

*   **Advanced Signal Processing:** Employs dynamic adaptive thresholding, exponential smoothing, and range filtering to guarantee stable readings
*   **Real-Time Data Visualization:** Features a 128x64 OLED screen that simultaneously displays the calculated BPM and a live scrolling waveform of the raw PPG signal
*   **Noise Rejection Architecture:** Integrates hardware-level high-pass and low-pass filters to successfully handle motion artifacts, baseline drift, and high-frequency electrical noise (like 50/60Hz power line interference)
*   **Smart Error Handling:** Automatically enters a "SCANNING" or "STABILIZING" state if the detected BPM falls outside the physiological norm (65-150 BPM) to prevent false readings

## 🛠️ Hardware Stack

*   **Microcontroller:** Arduino (utilizes the built-in ADC for analog-to-digital conversion)
*   **Optical Sensor:** A transmissive setup combining a 660nm Red LED and an ST-1KLA phototransistor
*   **Amplification Stage:** An LM358 operational amplifier configured as a non-inverting amplifier, utilizing a 1MΩ feedback resistor and 1kΩ input resistor to achieve an ultra-high gain of 1001
*   **Filtering:** A 22µF capacitor acts as a high-pass filter to block DC offset, while a 0.1µF (104) ceramic capacitor serves as a low-pass filter[cite: 2].
*   **Display:** 128x64 OLED Display operated via the Adafruit SSD1306 library

## 🧠 Software & Algorithm Logic

1.  **Signal Acquisition:** The Arduino continuously samples the amplified analog voltage
2.  **Smoothing:** Applies an exponential smoothing filter to mitigate high-frequency fluctuations
3.  **Peak Detection:** Calculates an adaptive threshold dynamically based on signal amplitude to accurately identify peaks and troughs
4.  **BPM Calculation:** Measures the Inter-Beat Interval (IBI) in milliseconds between successive peaks and divides 60,000 by the IBI to extract the heart rate[cite: 2].

## 📊 Performance & Validation

During controlled 10-minute testing trials across 6 diverse participants, HeartSync was benchmarked against the commercial Mi Band 8 
*   The system maintained a consistent error margin of just 8% to 10% (averaging ~9%)
*   Standard deviation analysis indicated highly stable and consistent BPM measurements over time

## 🚀 Future Roadmap

*   **Hardware Expansion:** Integrating additional sensors to measure supplementary metrics like blood oxygen saturation (SpO2)
*   **Algorithmic Refinement:** Improving the calibration process to account for individual user variations like skin tone and body composition
*   **Environmental Resilience:** Upgrading components to further reduce sensitivity to ambient light changes and high electromagnetic interference

---

**👨‍💻 Development Team:**
Md Nazmun Nur (Lead), Asif Khan, Joy Saha, Sakib Hasan Sony, Hasanur Jaman Joni, Siam Ahammed, MD. Mahmudul Hasan[cite: 2].  
**🏛️ Institution:** Department of Electrical and Electronics Engineering, American International University Bangladesh (AIUB)[cite: 2].
