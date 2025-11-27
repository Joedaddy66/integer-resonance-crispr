import pandas as pd
import matplotlib.pyplot as plt
import math
import sympy as sp
import re
import sys
from typing import Tuple

BASE4 = {"A": 0, "C": 1, "G": 2, "T": 3}
CODON2INT = {
    a + b + c: BASE4[a] * 16 + BASE4[b] * 4 + BASE4[c]
    for a in "ACGT" for b in "ACGT" for c in "ACGT"
}

# Constants for sequence analysis
CODON_SPACE = 64  # Number of possible codons (4^3)
CODON_PAIR_LENGTH = 6  # Two codons for semiprime analysis
PROTOSPACER_START = 4  # Start index for protospacer in 30mer
PROTOSPACER_END = 27  # End index for protospacer in 30mer (20nt + 3nt PAM)
PERCENTAGE_THRESHOLD = 1.5  # Threshold to detect percentage vs decimal format


def codon_to_int(codon: str) -> int:
    codon = codon.upper()
    if len(codon) != 3 or any(n not in BASE4 for n in codon):
        raise ValueError(f"Invalid codon: {codon!r}")
    return CODON2INT[codon]


def semiprime_factors(n: int) -> Tuple[int, int]:
    factors = sp.factorint(n)
    if len(factors) != 2 or any(exp != 1 for exp in factors.values()):
        raise ValueError("Not a semiprime")
    p, q = factors.keys()
    return int(p), int(q)


def fingerprint(p: int, q: int) -> float:
    a = (p + q) / 2
    m = p * q
    delta = abs(p - q)
    if a <= 1:
        return 0.0
    lam = delta**2 / (m * math.log(a))
    return lam


def analyze_sequence_for_score(seq: str, step: int = 1, pam: str = 'NGG') -> float:
    pam_re = re.compile(f"^{pam.upper().replace('N', '[ACGT]')}$")
    total_lambda = 0.0
    protospacer = seq[:20]
    pam_seq_from_input = seq[20:23]
    if not (len(pam_seq_from_input) == 3 and pam_re.fullmatch(pam_seq_from_input)):
        return 0.0
    for i in range(0, len(protospacer) - CODON_PAIR_LENGTH + 1, step):
        try:
            c1 = codon_to_int(protospacer[i : i + 3])
            c2 = codon_to_int(protospacer[i + 3 : i + 6])
            N = c1 * CODON_SPACE + c2
            p, q = semiprime_factors(N)
            total_lambda += fingerprint(p, q)
        except (ValueError, TypeError):
            continue
    return total_lambda


def run_validation(data_path: str, output_filename: str):
    print(f"Loading dataset from {data_path}...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"\nERROR: '{data_path}' not found.", file=sys.stderr)
        sys.exit(1)

    df.rename(columns={'Percent Peptide': 'Lab_Efficiency', 'predictions': 'Azimuth_Score'}, inplace=True)
    if 'Lab_Efficiency' not in df.columns:
        print("\nERROR: Could not find 'Lab_Efficiency' or 'Percent Peptide' column.", file=sys.stderr)
        sys.exit(1)
    df['Lab_Efficiency'] = pd.to_numeric(df['Lab_Efficiency'], errors='coerce')
    if df['Lab_Efficiency'].max() > PERCENTAGE_THRESHOLD:
        df['Lab_Efficiency'] = df['Lab_Efficiency'] / 100.0
    print("Calculating Semiprime λ Scores...")
    df['Aggregate_Lambda_Score'] = df['30mer'].apply(
        lambda x: analyze_sequence_for_score(str(x)[PROTOSPACER_START:PROTOSPACER_END].upper())
    )
    print("Calculation complete.")
    print(f"Generating plot and saving to {output_filename}...")
    plt.figure(figsize=(12, 8))
    plt.scatter(df['Aggregate_Lambda_Score'], df['Lab_Efficiency'], alpha=0.5)
    plt.title('Semiprime λ Score vs. Lab Efficiency (Smoke Test)')
    plt.xlabel('Aggregate Semiprime λ Score')
    plt.ylabel('Actual Lab Efficiency (Normalized)')
    plt.grid(True)
    plt.savefig(output_filename)
    print("Plot generated successfully.")
    plt.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_csv = sys.argv[1]
        output_plot = "ci_smoke_test_plot.png"
    else:
        print("Usage: python analyze.py <path_to_csv>", file=sys.stderr)
        sys.exit(1)

    run_validation(input_csv, output_plot)
