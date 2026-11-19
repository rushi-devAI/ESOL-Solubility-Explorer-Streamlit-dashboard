This dashboard explores the relationship between molecular structure and aqueous solubility ($\log S$) using the Delaney (ESOL) dataset. It allows users to filter compounds by structural descriptors and compare experimental solubility measurements against ESOL model predictions.
## Project Overview
This dashboard explores the relationship between molecular structure and aqueous solubility ($\log S$) using the Delaney (ESOL) dataset. It allows users to filter compounds by structural descriptors and compare experimental solubility measurements against ESOL model predictions.
## Dataset
- **Source:** Delaney Processed Dataset (`delaney-processed.csv`)
  ## Dashboard Features
- **Filters:** Filter compounds by **Number of Rings**, **Number of H-Bond Donors**, and **Solubility Class** (`Soluble`, `Moderate`, `Poorly Soluble`).
- **Multiple Views:**
  - *Overview & Parity:* Model parity scatter plot, solubility distribution histogram, and molecular weight box plot.
  - *Ring & H-Bond Analysis:* Polar surface area scatter plot and solubility distributions grouped by ring count and H-bond donors.
  - *Dataset Records:* Searchable table of filtered compound entries.

  ## How to Run Locally
```bash
git clone [https://github.com/](https://github.com/)<your-username>/<your-repo-name>.git
cd <your-repo-name>
pip install -r requirements.txt
streamlit run app.py
