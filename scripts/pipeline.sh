#!/bin/bash

# NGS Variant Calling Pipeline
# Data: E. coli K-12 (SRR1553607)

FASTQ1=data/SRR1553607_1.fastq
FASTQ2=data/SRR1553607_2.fastq
REF=reference/ecoli_k12.fasta
OUT=results

mkdir -p $OUT

echo "========================================="
echo "Step 1: Quality Control with FastQC"
echo "========================================="
fastqc $FASTQ1 $FASTQ2 -o $OUT

echo "========================================="
echo "Step 2: Indexing reference genome"
echo "========================================="
bwa index $REF

echo "========================================="
echo "Step 3: Aligning reads to reference"
echo "========================================="
bwa mem $REF $FASTQ1 $FASTQ2 > $OUT/aligned.sam

echo "========================================="
echo "Step 4: Converting SAM to BAM"
echo "========================================="
samtools view -Sb $OUT/aligned.sam > $OUT/aligned.bam

echo "========================================="
echo "Step 5: Sorting BAM"
echo "========================================="
samtools sort $OUT/aligned.bam -o $OUT/aligned_sorted.bam

echo "========================================="
echo "Step 6: Indexing BAM"
echo "========================================="
samtools index $OUT/aligned_sorted.bam

echo "========================================="
echo "Step 7: Variant Calling"
echo "========================================="
bcftools mpileup -f $REF $OUT/aligned_sorted.bam | \
bcftools call -mv -Ov -o $OUT/variants.vcf

echo "========================================="
echo "Pipeline finished!"
echo "Results are in the $OUT folder"
echo "========================================="

echo "========================================="
echo "Step 8: Filtering low quality variants"
echo "========================================="
bcftools filter -i 'QUAL>20' results/variants.vcf > results/variants_filtered.vcf

echo "Filtered variants saved to results/variants_filtered.vcf"

# Count variants before and after filtering
BEFORE=$(grep -v "^#" results/variants.vcf | wc -l)
AFTER=$(grep -v "^#" results/variants_filtered.vcf | wc -l)

echo "Variants before filtering: $BEFORE"
echo "Variants after filtering:  $AFTER"
echo "========================================="
