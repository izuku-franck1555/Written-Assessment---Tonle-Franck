### **Written Assessment – Tonle Franck**  

#### **Overview**  
This repository contains my submission for the climate data analysis, spatial modeling, and crop modeling assessment. The analysis examines the impact of climate hazards on crop production in India using sub-national production and climate datasets.  

#### **Repository Structure**  

- 📄 **Full-Notebook-Version.pdf** – Complete version of the Jupyter Notebook, rendered as a PDF.  
- 📄 **Summary-Written-Assessment-Tonle-Franck.pdf** – Concise summary of the methodology, results, and key insights.  
- 📂 **data.zip/** – Contains climate and crop production datasets:  
  - `climate/` – Raw, processed, and aggregated climate data with hazard indicators.  
  - `country_apy_fao_1956-2014.csv` & `county_a_fao_1947-2014.csv` – Crop production data.  
  - `district_apy_interpolated_1956-2008.csv` – Interpolated sub-national crop yield data.  
  - `india_districts_71.*` – Shapefiles for spatial analysis.  
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
1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Jupyter Notebook:  
   ```bash
   jupyter notebook climate_crops_india_analysis.ipynb
   ```