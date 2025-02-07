### **Written Assessment – Tonle Franck**  

#### **Overview**  
This repository contains my submission for the climate data analysis, spatial modeling, and crop modeling assessment. The analysis examines the impact of climate hazards on crop production in India using sub-national production and climate datasets.  

#### **Repository Structure**  

- 📄 **Full-Notebook-Version.pdf** – Complete version of the Jupyter Notebook, rendered as a PDF.  
- 📄 **Summary-Written-Assessment-Tonle-Franck.pdf** – Concise summary of the methodology, results, and key insights.  
- 🌍 **Dataset Download** – The dataset is too large to be stored on GitHub. It can be downloaded from Google Drive:  
  **[Download Data (4GB)](https://drive.google.com/file/d/1yKSA2rzKDX0VV9-3qnrRMqgAAG5uYtf-/view?usp=sharing)**  
  - After downloading, extract the files and place them in a `data/` directory within this repository.  
- 📂 **climate_crops_india_analysis.ipynb** – Jupyter Notebook documenting the full analysis workflow.  
- 📜 **era5-download-manager.py** – Script for downloading ERA5 climate data.  
- 📜 **requirements.txt** – Dependencies for reproducing the analysis.  

#### **Key Components**  
1. **Data Processing** – Downloaded and preprocessed climate and crop production data.  
2. **Climate Hazard Indicator** – Computed a relevant climate hazard metric affecting crop yield.  
3. **Statistical Analysis** – Modeled the relationship between climate hazards and crop production.  
4. **Visualization & Interpretation** – Generated maps and plots to explain the findings.  
5. **Reporting** – Summarized insights in a structured document for both technical and non-technical audiences.  

#### **How to Run**  
1. **Download and extract the dataset**  
   - Download the dataset from **[Google Drive](https://drive.google.com/file/d/1yKSA2rzKDX0VV9-3qnrRMqgAAG5uYtf-/view?usp=sharing)**.  
   - Extract the contents and place them inside a `data/` directory in this repository.  

2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Jupyter Notebook:**  
   ```bash
   jupyter notebook climate_crops_india_analysis.ipynb
   ```