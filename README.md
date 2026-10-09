# Data Mining - Data Preparation Homework

This repository contains the Python implementation of the **3-4-5 Data Transformation Algorithm** as described in the course lecture slides.

## Files Included

1. `homework_submission.py`: The main Object-Oriented Python script that implements the algorithm, generates a clean terminal report, and plots the data distribution.
2. `homework_chart.png`: The generated high-resolution bar chart showing the frequency distribution of the data groups and highlighting the 5% trimmed outliers.

## How to Run

Ensure you have Python 3 installed, along with the `matplotlib` library for the visualization.

```bash
# Install required dependencies
pip install matplotlib

# Run the algorithm
python homework_submission.py
```

## Implementation Details

This script rigorously follows the instructions from the provided lecture slides (Slides 48-52). Specifically:
- **Tail Trimming:** Accurately calculates 5% of the 60 items (3 items) and trims them from the lower and upper bounds of the sorted dataset.
- **Interval Calculation (IV):** Calculates the Most Significant Digit (MSD) unit and derives the correct Interval Value (IV = 5).
- **Splitting Criterion:** In strict accordance with the slide examples, the group width uses the **exact, unrounded** minimum and maximum values `(347 - (-94)) / 5 = 88.2` rather than the rounded boundaries, ensuring maximum analytical precision for the continuous data split. 
- **Validation:** Performs a strict length validation to ensure exactly 60 items are categorized at the end.
