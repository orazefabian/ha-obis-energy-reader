# OBIS Energy Reader

A custom Home Assistant integration to read energy measurement data in the OBIS standard from a configurable JSON endpoint (e.g., from an ESP32 or smart meter).

## Features
- Reads OBIS energy and power values from a user-defined HTTP JSON endpoint
- Exposes each OBIS field as a Home Assistant sensor (e.g., 1.8.0, 2.8.0, 1.7.0, etc.)
- Provides binary sensors for importing/exporting power
- Includes a (dummy) switch for uptime reset example

## Supported OBIS Fields
- 1.8.0: Total active energy consumed (import)
- 2.8.0: Total active energy exported (export)
- 3.8.0: Total positive reactive energy imported
- 4.8.0: Total negative reactive energy exported
- 1.7.0: Instantaneous active power (import)
- 2.7.0: Instantaneous active power (export)
- 16.7.0: Instantaneous total active power
- timestamp, uptime, UTC

## Installation

### Option 1: HACS (Recommended)
1. Open **HACS** in your Home Assistant instance.
2. Go to **Integrations**.
3. Click the **three dots menu** in the top right corner and select **Custom repositories**.
4. Add this repository URL: `https://github.com/orazefabian/ha-obis-energy-reader`
5. Set the category to **Integration**.
6. Click **Add**.
7. Find **OBIS Energy Reader** in the HACS integrations list and click **Download**.
8. Restart Home Assistant.

### Option 2: Manual Installation
1. Copy the `obis_energy_reader` folder to your Home Assistant `custom_components` directory:
   ```
   /config/custom_components/obis_energy_reader
   ```
2. Restart Home Assistant.

## Configuration
1. Go to **Settings > Devices & Services > Integrations** in Home Assistant.
2. Click **Add Integration** and search for **OBIS Energy Reader**.
3. Enter your OBIS JSON endpoint URL and credentials.
4. After setup, sensors and entities will be available in Home Assistant.

## Example JSON Endpoint
```
{
  "1.8.0": "9463429",
  "2.8.0": "11062",
  "3.8.0": "17773",
  "4.8.0": "4179110",
  "1.7.0": "433",
  "2.7.0": "0",
  "16.7.0": "433",
  "timestamp": "2025-07-06T20:37:05",
  "uptime": "0000:00:06:30",
  "UTC": "2025-07-06T18:37:00"
}
```

## More Information
- [OBIS Standard (Wikipedia)](https://en.wikipedia.org/wiki/OBIS_code)
- [GitHub Repository](https://github.com/orazefabian/ha-obis-energy-reader)

---
This integration is not affiliated with Home Assistant or any meter manufacturer.
