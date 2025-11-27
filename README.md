# Integer Resonance: A CRISPR Discovery Platform for "Forbidden Zone" Targets

> "Standard models are ranking tools; the Semiprime λ Pipeline is a decision engine for undruggable genomes."

**What We Do:** Identify viable CRISPR targets in repetitive genomic regions (CAG repeats, low-complexity sequences) that standard tools systematically exclude.

**Why It Matters:** Billions in R&D are stalled because computational tools treat 20-30% of the genome as "design-dead zones," eliminating therapeutic opportunities for repeat-expansion diseases.

---

## The Problem: Algorithmic Blind Spots in CRISPR Design

Current gRNA design tools use heuristic rules to filter out repetitive sequences, creating **therapeutic blind spots** for diseases like Huntington's, Fragile X, and C9orf72 ALS.

## The Innovation: Integer Resonance Scoring

We treat DNA as **integer compositions** and measure algebraic stability via semiprime factorization. Our `λ` score captures a hidden structural feature of the sequence, allowing us to find viable targets where others cannot.

**Hypothesis:** Cas9 interacts with sequence *context*, not just *identity*. Our scoring captures this hidden layer.

---

## Validation: Doench 2016 Benchmark (11,064 Sequences)

Our model demonstrates a high-precision "NO-GO" filter (the "Left Wall" at λ=0), eliminating non-viable candidates pre-experimentally and proving it is an **orthogonal signal**, not a proxy for GC content.

![Comparative Analysis](results/comparative_validation_plot.png)

---

## Proof of Principle: Huntington's Disease (HTT)

We identified **viable gRNA candidates within the pathogenic HTT CAG repeat tract**—a "no-fly zone" for standard tools, creating novel IP in uncontested white space.

---

## Current Status & Opportunity

*   **✅ Completed:** Computational validation on 11K+ benchmark sequences.
*   **🔄 In Progress:** Provisional patent filing & wet-lab partner outreach.
*   **📈 Roadmap:** Validate HTT candidates -> Scale to 3-5 other repeat diseases -> Launch SaaS platform.

This is a **platform play** with a portfolio of targets, not a single high-risk asset.

## Installation & Usage
```bash
git clone https://github.com/Joedaddy66/integer-resonance-crispr.git
cd integer-resonance-crispr
pip install -r requirements.txt

# Download full Doench 2016 dataset and place in root
# python analyze.py
```

## Seeking
Wet Lab Partners, Strategic Investors, and Pharma Partnerships.

Contact: [Your Email Here]
