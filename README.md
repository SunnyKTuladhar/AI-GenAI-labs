# AI-GenAI-labs

A collection of hands-on labs for the AI/ML course in LFConnect. This repository contains Jupyter notebooks, datasets, and supplemental images used for teaching core ML concepts including linear regression, non-linear regression and overfitting, logistic regression, k-means clustering, and the perceptron.

---

## Contents

- 01-Linear-Regression — notebook and datasets for linear regression examples and exercises
- 02-Nonlinear Regression and Overfitting — experiments demonstrating under/overfitting and model selection
- 03-Logistic-Regression — classification examples and datasets
- 04-K-Means-Clustering — k-means clustering examples and visualizations
- 05-Perceptron — perceptron implemented from scratch, with scikit-learn, Keras, and PyTorch
- 06-Mlp — MLP lab notebook, gradient descent comparison (batch/SGD/mini-batch), activation functions (linear vs ReLU), and a hand digit classification project with a Streamlit app (`Social_Network_Ads.csv` used by the gradient descent notebook)

Each lab folder contains at least one .ipynb notebook and sample data files (CSV/ TXT) used in the exercises.

---

## Prerequisites

- Python 3.11 or 3.12 (the notebooks were authored on these versions)
- Jupyter Notebook or JupyterLab

Required Python packages are listed in `requirements.txt`:
- jupyterlab
- numpy
- pandas
- scipy
- scikit-learn
- matplotlib
- seaborn
- tensorflow (05-Perceptron, 06-Mlp)
- streamlit (only for 06-Mlp/Project)
- Pillow (only for 06-Mlp/Project)

---

## Setup (Windows)

1. Create and activate a virtual environment:

   python -m venv .venv
   .venv\Scripts\activate

   On macOS/Linux use `source .venv/bin/activate` instead.

2. Install required packages:

   pip install --upgrade pip
   pip install -r requirements.txt

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
- Versions in `requirements.txt` are minimums, not pins.

---

Maintainer: SunnyKTuladhar , Samir Dahal
