# NeoPupil <img src="NeoPupil.png" width="5%">

*A GUI Tool for Eye-Tracking Data Visualisation*

**NeoPupil** is a Python-based tool with a graphical user interface (GUI) for analysing and visualising eye-tracking data from the [Neon eye-tracking system](https://pupil-labs.com/products/neon) (Pupil Labs GmbH).

It is specifically designed for handling **Time Series Data** exported from [Pupil Cloud](https://cloud.pupil-labs.com/), and supports multiple types of data files typically generated during an eye-tracking session.

NeoPupil was inspired by the [SPEED software](https://github.com/danielelozzi/SPEED).

---

## 📁 Supported Input Files

NeoPupil requires the following `.csv` files exported from Pupil Cloud:

- `3d_eye_states.csv`
- `blinks.csv`
- `events.csv`
- `fixations.csv`
- `gaze.csv`
- `saccades.csv`

These files must follow the default schema of Pupil Labs' export structure (timestamps in nanoseconds, labeled events, gaze coordinates in pixels, etc.).

---

## 📊 Features & Visualisations

NeoPupil can generate a wide variety of plots, helping researchers extract insights from visual attention data. The visuals include:

### 🔵 General
- **Blink duration over time** with event annotations
- **Histogram of blink durations**

### 🔁 Event-based Analysis

For each pair of consecutive events (between a defined start and end event), NeoPupil computes and visualises:

- Mean and standard deviation of:
  - Blinks
  - Fixations
  - Saccades

- Frequency (per second) of:
  - Blinks
  - Fixations
  - Saccades

### ⏱ Time Binned Analysis (custom interval ≤ 60s)
- Mean duration per bin (for blinks, fixations, saccades)
- Count per bin (occurrence number per interval)

### 👁 Gaze Path Visualisation
- Individual gaze paths between pairs of events
- Global gaze path overview during the selected interval

### 🔍 Pupils Diameter Visualisation
- **Event-based analysis**  
  For each pair of consecutive events, computes and plots the **mean pupil diameter** (average of left and right eye) between these events.  

- **Time-binned analysis**  
  For a user-defined interval (≤ 60 s), computes and plots the **mean pupil diameter** within each time bin.
  
Each plot is saved as an image in the selected output folder.

---

## 🖥️ User Interface

NeoPupil includes an intuitive GUI built using `CustomTkinter`. The interface includes:
1. **Output Folder** — choose where plots will be saved 
2. **Input Selection** — load the CSV files you want to analyse    
3. **Event Interval** — select the start and end event to define the time window  
4. **Customisation** — pick plot colour and time bin size (≤ 60 seconds)  
5. **Generate** — launch plot generation and get notified when done

All GUI controls are grouped logically to simplify workflow for researchers and non-programmers alike.

---

## 🧰 Installation

1. Clone the repository:

```bash
git clone https://github.com/matthieukeruzoret/NeoPupil.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python GUI.py
```

---
## 📚 Documentation
Full documentation and user guide are available [here](https://matthieukeruzoret.github.io/NeoPupil/).

Includes:

- Setup instructions
- GUI navigation guide
- Application Programming Interface (API)

---
## ✍️ Author & Citation
**Author**: Matthieu KÉRUZORET, Polytech Nice-Sophia – Applied Mathematics & Modeling (MAM4)

If you use NeoPupil in your work or research, please cite it as:
   
- KÉRUZORET, M. (2025). NeoPupil: A GUI Tool for Eye-Tracking Data Visualisation. GitHub. https://github.com/matthieukeruzoret/NeoPupil

It is also requested to cite Pupil Labs publication, as requested on their website https://docs.pupil-labs.com/neon/data-collection/publications-and-citation/

- Baumann, C., & Dierkes, K. (2023). Neon accuracy test report. Pupil Labs, 10.

--- 

## 📚 Acknowledgements

NeoPupil was inspired by and can complement the SPEED software, offering additional or alternative features for eye-tracking data analysis:

- Lozzi, D.; Di Pompeo, I.; Marcaccio, M.; Ademaj, M.; Migliore, S.; Curcio, G. SPEED: A Graphical User Interface Software for Processing Eye Tracking Data. NeuroSci 2025, 6, 35. https://doi.org/10.3390/neurosci6020035 

- Lozzi, D.; Di Pompeo, I.; Marcaccio, M.; Alemanno, M.; Krüger, M.; Curcio, G.; Migliore, S. AI-Powered Analysis of Eye Tracker Data in Basketball Game. Sensors 2025, 25, 3572. https://doi.org/10.3390/s25113572

---

## 🤖 Use of AI
AI tools were used to assist the development of NeoPupil.

---
## 📄 License

Distributed under the [MIT License](LICENSE).  

Feel free to use, modify, and distribute this software in accordance with the license terms.