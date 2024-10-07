# Vortex ROV Code Repository

Welcome to the repository for the Vortex ROV software! This README will guide you through the prerequisites and file structure of the ROV's software.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Repository Structure](#repository-structure)

## Introduction

The Vortex ROV software is responsible for managing the ROV's onboard systems, including navigation, control, sensor data processing, and communication with the Topside Control Unit (TCU). This software ensures that the ROV operates effectively during underwater missions, enabling precise control, data collection, and task execution.

## Installation

To set up the ROV software on your development environment, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Vortex-ROV/ROV-Code.git
   cd ROV-Code
   ```
2. **Create and Activate a Virtual Environment:**

   It's a good practice to use a virtual environment to manage dependencies. Run the following commands to create and activate one:

   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     
3. **Install Packaged Dependencies:**
   ```bash
   pip install .
   ```

4. **Run the ROV Software:**
   ```bash
   python main.py
   ```

## Repository Structure

- **`/src`:** Core source code for navigation, control, and sensor data processing.
- **`/tests`:** Test cases to validate the software's functionality and performance.
- **`main.py`:** Main script used to launch the ROV software.
- **`ROV.toml`:** Configuration file for packaging ROV code.
