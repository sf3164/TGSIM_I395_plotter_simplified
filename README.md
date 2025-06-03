# Vehicle Trajectory Visualization Tool simplified version (for TGSIM I395 Data)

This is a simplified python GUI-based tool for plotting **vehicle trajectories** using TGSIM I395 data. Designed for fast and direct use, this version allows users to manually input multiple vehicle IDs and generate interactive Plotly visualizations that include detailed lane and trajectory data.

## Features

- Manually input **comma-separated vehicle IDs** (e.g., `1, 2`).
- Error handling for:
  - Non-numeric inputs
  - Vehicle IDs not found in selected run
- Generates interactive Plotly plots with hover info:
  - ID
  - Time
  - Lane
  - Speed
  - Acceleration
- Displays all **lane boundaries** with labels for road context.

## Example Output

The tool produces an HTML file (`I395_Simplified_Plot.html`) displaying the interactive plot.
![image](https://github.com/user-attachments/assets/a52d7376-5ed1-4351-ae1c-c324dfaed0f6)


## File Structure

```bash
.
├── TGSIM_I395.csv            # Main trajectory dataset
├── boundaries/
│   ├── I395_boundaries.csv
├── plotter.py           # Python file with Tkinter GUI and plotting code
└── README.md
```

## Dependencies

- `pandas`
- `plotly`
- `matplotlib`
- `tkinter` (built-in in most Python distributions)

You can install the required packages with:

```bash
pip install pandas plotly matplotlib
```

> `tkinter` is usually included with standard Python installations. If you're using Linux and don't have it installed, try:
>
> ```bash
> sudo apt-get install python3-tk
> ```

## How to Use

1. Download the TGSIM I395 main dataset and the boundaries files from the following website:
https://data.transportation.gov/Automobiles/Third-Generation-Simulation-Data-TGSIM-I-395-Traje/97n2-kuqi/about_data
2. Rename the main dataset to TGSIM_Stationary.csv and move it to the same directory as the `plotter.py` script.
3. In the same directory as `plotter.py`, create a new folder named `boundaries`, and move all the centerline files into this folder.
4. Launch the Python to run `plotter.py` and run all cells.
5. A GUI window will appear.
6. Enter one or more vehicle IDs (comma-separated).
7. Click **Plot** to generate the interactive plot.
   

The plot will open in a browser window and also be saved as `I395_Simplified_Plot.html`.


## Notes

- Centerline CSVs must be named in the format:  
  `I395_boundaries.csv`
- These files must be placed in the `boundaries/` directory relative to the notebook.
- The code currently writes to a fixed output file (`I395_Simplified_plot.html`) — feel free to modify this for custom output names.

## License

This project is open-source

## Author

David Feng  
Ph.D. Student, UVA Civil & Environmental Engineering Dept.  <br />
Graduate Research Assistant, Turner-Fairbank Highway Research Center <br />




