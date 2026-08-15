# AI-GenAI-labs

A collection of hands-on labs for the AI/ML course in LFConnect. This repository contains Jupyter notebooks, datasets, and supplemental images used for teaching core ML concepts including linear regression, non-linear regression and overfitting, logistic regression, and k-means clustering.

---

## Contents

- 01-Linear-Regression — notebook and datasets for linear regression examples and exercises
- 02-Nonlinear Regression and Overfitting — experiments demonstrating under/overfitting and model selection
- 03-Logistic-Regression — classification examples and datasets
- 04-K-Means — k-means clustering examples and visualizations

Each lab folder contains at least one .ipynb notebook and sample data files (CSV/ TXT) used in the exercises.

---

## Prerequisites

- Python 3.10+ (3.11 recommended)
- Jupyter Notebook or JupyterLab

Recommended Python packages (install below):
- jupyter
- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn

There is no centralized requirements.txt in this repository; installing the packages above is sufficient for running the notebooks.

---

## Setup (Windows)

1. Create and activate a virtual environment:

   python -m venv .venv
   .venv\Scripts\activate

2. Install required packages:

   pip install --upgrade pip
   pip install jupyter numpy pandas scikit-learn matplotlib seaborn

3. Start Jupyter Lab / Notebook from the repository root:

   jupyter lab
   # or
   jupyter notebook

Then open the desired lab notebook (for example: `01-Linear-Regression\01-Linear-Regression.ipynb`).

---

## Running the labs

- Open the notebook in Jupyter and run cells in order.
- Data files are stored alongside each notebook (e.g., `01-Linear-Regression/data.csv`).
- If a cell fails due to a missing package, install it into your active environment and restart the kernel.

---

## Contributing

Contributions, improvements, and fixes are welcome:
1. Fork the repository.
2. Create a topic branch for your changes.
3. Open a pull request against `main` with a clear description of changes.

Please avoid committing virtual environments (such as `.venv`) or large binary artifacts.

---

## Notes

- This README targets the `main` branch and serves as the primary guide for students and instructors.
- If you want a requirements.txt or automated environment setup, open an issue or submit a PR adding it.

---

Maintainer: SunnyKTuladhar

