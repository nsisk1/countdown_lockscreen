# countdown_lockscreen
Custom Lockscreen challenge

## Project files

- **`generate_lockscreen.py`** (opened in Canvas): Standalone script using Pillow (`PIL`) and NumPy to procedurally generate the 1080×1920 (9:16) wallpaper. It renders the dark matte carbon background, telemetry corner brackets, glowing "T-MINUS 40:00:00" headline, amber subtitle, and the 5-segment milestone gauge (`T-5D` through `T-1D`) with configurable active stage highlighting.
- **`t_minus_tracker.py`** (opened in Canvas): CLI dashboard that computes exact remaining T-minus hours, prints your intra-day schedule checkpoints, and exports an iCalendar (`.ics`) file.
- **`t_minus_lockscreen.png`**: The rendered high-resolution 9:16 lock screen ready to set on your phone.
- **`t_minus_accountability.ics`**: Importable calendar schedule for your 8:30 AM daily milestone check-ins.

## Installation

```bash
pip install Pillow numpy
```

## Generate the lock screen

Runs with defaults (`T-5D` active, `T-40:00:00`):

```bash
python generate_lockscreen.py
```

For example, update the wallpaper on Wednesday with `T-3D` active:

```python
from generate_lockscreen import generate_lockscreen

generate_lockscreen(
    output_path="lockscreen_wednesday.png",
    main_text="T-MINUS 24:00:00",
    subtitle="TARGET: FRIDAY • 8H / STAGE",
    active_stage=3,  # Fills T-5D, T-4D, and T-3D
)
```

Run the tracker dashboard and export the accountability calendar with:

```bash
python t_minus_tracker.py
```
