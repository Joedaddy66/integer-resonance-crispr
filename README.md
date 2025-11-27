# Semiprime λ Scoring: An Integer Resonance Model for gRNA Efficacy Prediction

**Status:** Computational Validation Complete | **Next Step:** Wet Lab Validation & Partnership

This repository contains the source code and validation results for the Semiprime λ Scoring model, a novel, first-principles method for predicting CRISPR gRNA efficacy. Our model has demonstrated a unique ability to identify high-potential gRNA targets in genomic regions that are systematically excluded by standard, thermodynamics-based algorithms.

---

### **The Hypothesis: Integer Resonance**

Current gRNA design tools are effective but conservative, creating "design-dead zones" in complex or repetitive genomic regions to avoid off-target risk. This leaves therapeutically critical targets, like the trinucleotide repeats in Huntington's disease, unexplored.

We hypothesize that gRNA efficacy is not solely a function of thermodynamic stability (GC content) but also of a sequence's **informational structure**. Our model translates DNA sequences into integers and uses a proprietary **Semiprime λ Score** to measure this "Integer Resonance."

A high `λ` score indicates a sequence possesses a specific, rare mathematical property, suggesting it is a high-potential candidate for successful cleavage, regardless of its thermodynamic profile.

### **Key Findings & Validation**

The model was validated against the full Doench 2016 benchmark dataset (n=11,064). The results prove three key advantages:

1.  **A High-Precision Filter:** The model's "Left Wall" phenomenon (where `λ Score = 0`) provides a definitive, binary "NO-GO" signal, correctly filtering out a vast majority of non-viable gRNA candidates with high precision.
2.  **An Orthogonal Signal:** The `λ` score is not a proxy for GC content. It successfully identifies "High-GC Traps" (high GC, low efficiency) as failures and "Low-GC Gems" (low GC, high efficiency) as successes.
3.  **A "Hidden Gem" Detector:** In a case study on the pathogenic exon of the *HTT* gene, the model's top-ranked candidate was located directly within the challenging CAG repeat expansion—a region standard tools refuse to analyze.

**This platform does not just rank candidates; it is a decision engine that finds value where other tools are blind.**

### **How to Run the Analysis**

1.  Clone this repository.
2.  Place the full `FC_plus_RES_withPredictions.csv` dataset in the root directory.
3.  Install dependencies: `pip install -r requirements.txt`
4.  Run the analysis script: `python analyze.py`

This will reproduce the validation plots from the raw data.

### **Citation & Contact**

A preprint detailing the full methodology and results is in preparation. For collaboration, investment, or licensing inquiries, please contact [Your Name/Email].
