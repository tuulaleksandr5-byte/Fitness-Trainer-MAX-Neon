# Fitness Trainer MAX — Neon Edition

A Russian-language Windows desktop fitness journal with a dark, neon-green interface.

Features: workout diary, food journal, seven-day activity chart, achievements, and preset fitness/wellness tips. Data are stored locally in the user's `FitnessTrainerMAX` folder. The helper contains preset advice rather than an online AI.

## Download the Windows app

1. Open [GitHub Actions](https://github.com/tuulaleksandr5-byte/Fitness-Trainer-MAX-Neon/actions).
2. Select **Build Windows EXE**.
3. Open the newest successful run (green check). If no run exists, select **Run workflow**.
4. Scroll to **Artifacts** and download **FitnessTrainerMAX-Windows**.
5. Extract the artifact ZIP and double-click `FitnessTrainerMAX.exe`.

Windows 10 and Windows 11 are supported by the packaged Tkinter app. Python is not required to run the packaged EXE.

## Build locally (optional)

```powershell
py -3.13 -m pip install pyinstaller
py -3.13 -m PyInstaller --onefile --windowed --name FitnessTrainerMAX fitness_trainer.py
```

The Windows EXE will be in `dist/FitnessTrainerMAX.exe`.
