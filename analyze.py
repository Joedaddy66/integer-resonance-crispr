import pandas as pd
import matplotlib.pyplot as plt
import math
import sympy as sp
import re
import sys
from typing import Tuple

# --- CORE LOGIC SEMIPRIME λ SCORING ---

BASE4 = {A 0, C 1, G 2, T 3}
CODON2INT = {
    a + b + c BASE4[a]  16 + BASE4[b]  4 + BASE4[c]
    for a in ACGT for b in ACGT for c in ACGT
}

def codon_to_int(codon str) - int
    codon = codon.upper()
    if len(codon) != 3 or any(n not in BASE4 for n in codon)
        raise ValueError(fInvalid codon {codon!r})
    return CODON2INT[codon]

def semiprime_factors(n int) - Tuple[int, int]
    factors = sp.factorint(n)
    if len(factors) != 2 or any(exp != 1 for exp in factors.values())
        raise ValueError(Not a semiprime)
    p, q = factors.keys()
    return int(p), int(q)

def fingerprint(p int, q int) - float
    a = (p + q)  2
    m = p  q
    delta = abs(p - q)
    if a = 1 return 0.0
    lam = delta2  (m  math.log(a))
    return lam

def analyze_sequence_for_score(seq str, step int = 1, pam str = 'NGG') - float
    pam_re = re.compile(f^{pam.upper().replace('N', '[ACGT]')}$)
    total_lambda = 0.0
    protospacer = seq[20]
    pam_seq_from_input = seq[2023]

    if not (len(pam_seq_from_input) == 3 and pam_re.fullmatch(pam_seq_from_input))
        return 0.0

    for i in range(0, len(protospacer) - 5, step)
        try
            c1 = codon_to_int(protospacer[i  i + 3])
            c2 = codon_to_int(protospacer[i + 3  i + 6])
            N = c1  64 + c2
            p, q = semiprime_factors(N)
            total_lambda += fingerprint(p, q)
        except (ValueError, TypeError)
            continue
            
    return total_lambda

# --- MAIN ANALYSIS & VISUALIZATION PIPELINE ---

def run_validation(data_path str, output_filename str)
    print(fLoading dataset from {data_path}...)
    try
        df = pd.read_csv(data_path)
    except FileNotFoundError
        print(fnERROR '{data_path}' not found.)
        return

    # Standardize column names
    rename_map = {
        'Percent Peptide' 'Lab_Efficiency', 
        'predictions' 'Azimuth_Score',
        'score_drug_gene_rank' 'Lab_Efficiency' # Handle different column names
    }
    df.rename(columns=lambda c rename_map.get(c, c), inplace=True)
    
    if 'Lab_Efficiency' not in df.columns
        print(nERROR Could not find a recognizable efficiency score column.)
        return
        
    df['Lab_Efficiency'] = pd.to_numeric(df['Lab_Efficiency'], errors='coerce')
    # Normalize if necessary
    if df['Lab_Efficiency'].max()  1.5
        df['Lab_Efficiency'] = df['Lab_Efficiency']  100.0

    print(Calculating Semiprime λ Scores for all sequences...)
    df['Aggregate_Lambda_Score'] = df['30mer'].apply(lambda x analyze_sequence_for_score(str(x)[427].upper()))
    print(Calculation complete.)

    if 'Azimuth_Score' in df.columns
        print(Generating comparative plot...)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 10), sharey=True)
        fig.suptitle('Comparative Analysis Standard Model vs. Semiprime λ Score', fontsize=24)

        # Plot 1 Standard Azimuth Model
        ax1.scatter(df['Azimuth_Score'], df['Lab_Efficiency'], alpha=0.3, s=15, c=df['Lab_Efficiency'], cmap='viridis')
        ax1.set_title('Standard Model (Azimuth) Performance', fontsize=18)
        ax1.set_xlabel('Predicted Score (Azimuth)', fontsize=14)
        ax1.set_ylabel('Actual Lab Efficiency (0 to 1)', fontsize=14)
        ax1.grid(True)

        # Plot 2 Our Semiprime λ Model
        scatter = ax2.scatter(df['Aggregate_Lambda_Score'], df['Lab_Efficiency'], alpha=0.3, s=15, c=df['Lab_Efficiency'], cmap='viridis')
        ax2.set_title('Our Model (Semiprime λ) Performance', fontsize=18)
        ax2.set_xlabel('Aggregate Semiprime λ Score', fontsize=14)
        ax2.axvline(x=0, color='red', linestyle='--', linewidth=2.5, label='THE FILTER (λ Score = 0)')
        ax2.grid(True)
        ax2.legend()
        
        fig.colorbar(scatter, ax=[ax1, ax2], label='Actual Lab Efficiency')
    else
        print(Generating single validation plot...)
        fig, ax = plt.subplots(figsize=(12, 10))
        scatter = ax.scatter(df['Aggregate_Lambda_Score'], df['Lab_Efficiency'], alpha=0.3, s=15, c=df['Lab_Efficiency'], cmap='viridis')
        ax.set_title('Semiprime λ Score vs. Lab Efficiency', fontsize=18)
        ax.set_xlabel('Aggregate Semiprime λ Score', fontsize=14)
        ax.set_ylabel('Actual Lab Efficiency (0 to 1)', fontsize=14)
        ax.axvline(x=0, color='red', linestyle='--', linewidth=2.5, label='THE FILTER (λ Score = 0)')
        ax.grid(True)
        ax.legend()
        fig.colorbar(scatter, ax=ax, label='Actual Lab Efficiency')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_filename)
    print(fPlot saved as '{output_filename}'.)
    plt.close()


if __name__ == '__main__'
    if len(sys.argv)  1
        # Allow running on a specific file from the command line
        input_csv = sys.argv[1]
        output_plot = custom_validation_plot.png
    else
        # Default to the main Doench dataset
        input_csv = 'FC_plus_RES_withPredictions.csv'
        output_plot = comparative_validation_plot.png
    
    run_validation(input_csv, output_plot)
