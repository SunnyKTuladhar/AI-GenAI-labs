<div align="center">

# AI-GenAI-labs

**Hands-on AI and machine learning labs for LFConnect**

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![License](https://img.shields.io/badge/Content-Educational-2ea44f)](https://github.com/SunnyKTuladhar/AI-GenAI-labs)

</div>

This repository contains practical notebooks, datasets, and supporting resources
for learning core machine learning, natural language processing, computer vision,
and generative AI concepts.

## Contents

- [Learning path](#learning-path)
- [Prerequisites](#prerequisites)
- [Getting started](#getting-started)
- [Running the labs](#running-the-labs)
- [Contributing](#contributing)

## Learning path

| Lab | Topics |
| --- | --- |
| [`01-Linear-Regression`](01-Linear-Regression) | Linear regression, datasets, and exercises |
| [`02-Nonlinear Regression and Overfitting`](02-Nonlinear%20Regression%20and%20Overfitting) | Underfitting, overfitting, and model selection |
| [`03-Logistic-Regression`](03-Logistic-Regression) | Classification and logistic regression |
| [`04-K-Means-Clustering`](04-K-Means-Clustering) | K-means clustering and visualizations |
| [`05-Perceptron`](05-Perceptron) | Perceptrons with scikit-learn, Keras, and PyTorch |
| [`06-Mlp`](06-Mlp) | MLPs, gradient descent, activation functions, and a Streamlit project |
| [`07-Computer-Vision`](07-Computer-Vision) | CNNs with TensorFlow, CIFAR-10, and YOLOv5 object detection |
| [`08-NLP`](08-NLP) | Tokenization, stemming, lemmatization, POS tagging, NER, BoW, TF-IDF, and Word2Vec |
| [`09-GenAI`](09-GenAI) | Gemini API, structured output, chat, function calling, and Tavily web search |

Each lab folder contains one or more notebooks and, where needed, sample data.
Some datasets are downloaded directly by the notebook.

## Prerequisites

- Python 3.11 or 3.12
- JupyterLab or Jupyter Notebook
- Git

The shared dependencies are defined in [`requirements.txt`](requirements.txt).
The GenAI notebook also uses:

```text
google-genai
pydantic
python-dotenv
tavily-python
```

## Getting started

### 1. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Start Jupyter

Run this command from the repository root:

```bash
jupyter lab
```

Then open the notebook for the lab you want to explore.

### 4. Configure GenAI API keys

The `09-GenAI` notebook uses Google Gemini and Tavily. Copy the environment
template and add your keys:

```powershell
Copy-Item 09-GenAI\.env.example 09-GenAI\.env
```

Set `GEMINI_API_KEY` for Gemini requests and `TAVILY_API_KEY` for the web-search
tool sections. The notebook loads these values with `python-dotenv`.

> **Keep your keys private.** Never commit `.env` files or API keys to the repository.

## Running the labs

1. Open a notebook in Jupyter.
2. Select the active `.venv` kernel.
3. Run the cells in order.
4. Keep data files alongside their notebooks when a lab requires local files.

For `09-GenAI`, run the package-installation cells or install the four
GenAI-specific packages listed above before running the notebook.

## Contributing

Contributions, improvements, and fixes are welcome:

1. Fork the repository.
2. Create a topic branch.
3. Make and test your changes.
4. Open a pull request against `main` with a clear description.

Please do not commit virtual environments, `.env` files, API keys, or large
generated artifacts.

## Notes

- This README targets the `main` branch and is the primary guide for students and instructors.
- Versions in `requirements.txt` are minimums, not pins.

## Contributors

- [SunnyKTuladhar](https://github.com/SunnyKTuladhar)
- [samirdahal888](https://github.com/samirdahal888)
