# AGENTS.md

## Repository overview

AI-GenAI-labs is an educational collection of Python and Jupyter notebook labs
covering classical machine learning, deep learning, computer vision, NLP, and
generative AI. Lab content is organized in numbered directories:

- `01-Linear-Regression` through `04-K-Means-Clustering`: foundational ML
- `05-Perceptron` and `06-Mlp`: neural networks and applied projects
- `07-Computer-Vision`: CNN and object-detection exercises
- `08-NLP`: natural language processing exercises
- `09-GenAI`: Google Gemini API and tool-calling exercises

## Environment and dependencies

- Use Python 3.11 or 3.12.
- Create a local virtual environment in `.venv`.
- Install shared dependencies with:

  ```bash
  python -m pip install -r requirements.txt
  ```

- The `09-GenAI` notebook additionally uses `google-genai`, `pydantic`,
  `python-dotenv`, and `tavily-python`.
- Do not commit `.venv`, `.env`, API keys, notebook checkpoints, or generated
  datasets and media.

## Working with notebooks

- Preserve the existing notebook structure and educational explanations.
- Run notebook cells in order when validating changes.
- Avoid committing large or unnecessary cell outputs.
- Keep datasets and supporting files in the lab directory that uses them.
- If a notebook requires credentials, document the variable names and use
  `.env.example`; never put real credentials in source or notebook cells.

## Code and documentation conventions

- Prefer clear, beginner-friendly Python over clever or compressed code.
- Match the surrounding notebook's naming, formatting, and teaching style.
- Keep changes focused on the requested lab or documentation.
- Update `README.md` when adding a lab, dependency, setup step, or user-facing
  workflow.
- Use relative links in Markdown documentation where possible.

## Validation

Before finishing a change:

1. Run `git diff --check`.
2. For Python changes, run the affected notebook cells or the smallest relevant
   executable check.
3. For dependency or setup changes, verify the documented commands and paths.
4. Confirm that no secrets, virtual-environment files, or unintended generated
   artifacts are included in the diff.

This repository does not currently define a dedicated automated test suite, so
notebook execution and focused smoke checks are the primary validation methods.

## Git workflow

- Do not reset, discard, or overwrite existing user changes.
- Keep commits focused and use descriptive messages.
- Do not push changes unless explicitly requested.
