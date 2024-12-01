# Automated Cyber Threat Intelligence for Closed Source Software Vulnerabilities

<div align="center">
  <img style="width: 100%;" src="banner.png" alt="Örnek Resim" width="300">
</div>

`cti-for-css` is a cutting-edge system designed to automate the production of cyber threat intelligence (CTI) for closed-source software vulnerabilities. Utilizing deep learning algorithms and an innovative function-as-sentence approach, this tool simplifies the detection and classification of software vulnerabilities.

## Key Features
- **Deep Learning Integration**: Supports MLP, OneDNN (One-Dimensional CNN), LSTM, and Bi-LSTM for vulnerability detection.
- **High Performance**: Achieved an F1 score of 82.4% and AUC score of 93.0%.
- **Fast Processing**: Classifies each vulnerability in under 0.32 seconds on average.
- **Comprehensive Dataset**: Can be trained using the SOSP and NDSS18 datasets, covering CWE-119 (buffer errors) and CWE-399 (resource management errors), or with other datasets formatted similarly to these.

## Function-as-Sentence Approach
The system introduces a novel method to represent binary data, reducing pre-processing workload and enhancing detection accuracy.

## Complementary Tools

We have made available the source code of `cti-for-css` along with three complementary tools:

1. **`cti-for-css-library-usage`**  
   Demonstrates how to integrate and use the `cti-for-css` system as a library within your projects.  
   [View](https://github.com/arikansm/cti-for-css/tree/main/Source%20Code/cti-for-css-framework-usage)

2. **`cti-for-css-gui`**  
   A user-friendly graphical interface for non-technical users to interact with the system.  
   [View](https://github.com/arikansm/cti-for-css/tree/main/Source%20Code/cti-for-css-gui-usage)

3. **`cti-for-css-stix-viewer`**  
   Visualises the produced cyber threat intelligence for easier interpretation.  
   [View Repository](https://github.com/arikansm/cti-for-css/tree/main/Source%20Code/cti-for-css-gui-usage/cti-for-css-stix-viewer)

## Publication

This project is based on a doctoral thesis and a research published in the **International Journal of Information Security**:

**(Article) Automating shareable cyber threat intelligence production for closed source software vulnerabilities: a deep learning-based detection system**  
[Read the publication here](https://link.springer.com/article/10.1007/s10207-024-00882-4)

**(Doctoral Thesis) Cyber Threat Intelligence with Deep Learning Based Vulnerability Detection System for Closed Source Software**  
[Not yet published](https://tez.yok.gov.tr/UlusalTezMerkezi/)

## Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/arikansm/cti-for-css.git
cd cti-for-css
pip install -r requirements.txt
