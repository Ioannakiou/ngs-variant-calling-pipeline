import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── Load VCF ──────────────────────────────────────────────
vcf_file = "results/variants.vcf"

variants = []

with open(vcf_file) as f:
    for line in f:
        if line.startswith("#"):
            continue
        fields = line.strip().split("\t")
        variants.append({
            "chromosome": fields[0],
            "position":   int(fields[1]),
            "ref":        fields[3],
            "alt":        fields[4],
            "quality":    float(fields[5]) if fields[5] != "." else None
        })

df = pd.DataFrame(variants)

# ── Summary ───────────────────────────────────────────────
print("=================================")
print("        VARIANT SUMMARY")
print("=================================")
print(f"Total SNPs found:     {len(df)}")
print(f"Mean quality score:   {df['quality'].mean():.2f}")
print(f"Min quality score:    {df['quality'].min():.2f}")
print(f"Max quality score:    {df['quality'].max():.2f}")
print("=================================")
print(df.head(10).to_string(index=False))

# ── Save CSV ──────────────────────────────────────────────
df.to_csv("results/variant_summary.csv", index=False)
print("\nCSV saved to results/variant_summary.csv")

# ── Plot: Variant positions along genome ──────────────────
plt.figure(figsize=(12, 4))
plt.scatter(df["position"], df["quality"], alpha=0.7, color="steelblue", edgecolors="navy")
plt.xlabel("Genomic Position")
plt.ylabel("Quality Score")
plt.title("SNP Positions along E. coli K-12 Genome")
plt.tight_layout()
plt.savefig("results/snp_plot.png", dpi=150)
print("Plot saved to results/snp_plot.png")

# ── Plot: REF vs ALT nucleotide changes ───────────────────
df["change"] = df["ref"] + "→" + df["alt"]
change_counts = df["change"].value_counts()

plt.figure(figsize=(10, 4))
change_counts.plot(kind="bar", color="steelblue", edgecolor="navy")
plt.xlabel("Nucleotide Change")
plt.ylabel("Count")
plt.title("SNP Types in E. coli Sample")
plt.tight_layout()
plt.savefig("results/snp_types.png", dpi=150)
print("Plot saved to results/snp_types.png")
