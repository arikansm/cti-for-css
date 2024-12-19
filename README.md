# Automated Cyber Threat Intelligence for Closed Source Software Vulnerabilities

<div align="center">
  <img style="width: 100%;" src="banner.png" alt="Örnek Resim" width="300">
</div>

`cti-for-css` is a cutting-edge system designed to automate the production of cyber threat intelligence (CTI) for closed-source software vulnerabilities. Utilizing deep learning algorithms and an innovative function-as-sentence approach, this tool simplifies the detection and classification of software vulnerabilities.

## Key Features
- **Deep Learning Integration**: Supports MLP, OneDNN, LSTM, and Bi-LSTM for vulnerability detection.
- **High Performance**: Achieved an F1 score of 82.4% and AUC score of 93.0% on the NDSS18 dataset (whole).
- **Fast Processing**: Classifies each vulnerability in under 0.32 seconds on average.
- **Comprehensive Dataset**: Can be trained using the SOSP and NDSS18 datasets, covering CWE-119 (buffer errors) and CWE-399 (resource management errors), or with other datasets formatted similarly to these.

## Function-as-Sentence Approach
The system introduces a novel method to represent binary data, reducing pre-processing workload and enhancing detection accuracy.

## Solution Method
The method begins with the preparation of the model. Subsequently, the binary files are converted to the requisite format, after which the classification process is performed. Subsequently, the cyber threat intelligence generation phase exports the intelligence file, utilizing the classification results.
 
In the initial stage, the model preparation phase, the model can be imported from a previously prepared file or generated from the dataset. In the event that a preexisting model is to be utilized, the pertinent model is loaded and the phase of binary file classification is initiated. In the event that the objective is to facilitate the learning of the model, the dataset is initially retrieved. The consistency of the pertinent dataset is then verified. At this stage, a comparison is conducted to ascertain the number of records in the dataset. In the event of a discrepancy between the number of functions and the number of labels, the program will be terminated immediately. As anticipated, when the number of functions and the number of labels are equivalent, the dataset is partitioned into training, validation, and test subsets. Prior to this partitioning, the data is shuffled to ensure that the measurements and learning are conducted independently of the data. Graphs illustrating the number of samples and label distributions for the partitioned subsets are generated and exported. The model is trained by applying vectorization to the subsets.
 
Vectorization is conducted through the utilisation of text vectorisation and embedding. In the process of text vectorization, each word is initially transformed into a distinct integer. Subsequently, the numerical values obtained through text vectorization are converted to vectors and presented as input to deep learning algorithms via the embedding process.
 
Text vectorization facilitates the execution of mathematical operations by converting words within a function, which is regarded as a sentence, into numerical values. The embedding process generates random numerical representations for each numerical value at the outset of the model's training process and updates these representations in accordance with performance metrics such as loss throughout the model's training. This approach facilitates the generation of the most effective number sequence, which can express the meaning and relationship bond between the words. The resulting number sequence, which is generated and refined for each word, represents a vector.
 
The words are derived from the binary data, which is then transformed into a format that aligns with the specifications of the pertinent data set. For example, let us assume that the first two words, "22|170,22" and "85|85," are obtained by converting the binary code. In this instance, a sentence "22|170,22 85|85, ..." is initially constructed, utilizing these words. Subsequently, the sentence is subjected to text vectorization in the vectorization phase and converted to the sequence [1, 2, 0, 0, …], wherein a specific index value is placed in place of each word. In order to achieve the desired output length, sentences of a specified length are populated with the value "0".
 
Subsequently, the data is subjected to an embedded representation process. Initially, random numerical values are generated for each word in order to create the embedded representation. To illustrate, for the sequence [1, 2, 0, 0, …], obtained through text vectorization, a random value sequence, for example [0.15852848, 0.01236449, 0.40107843, …], is generated for the value "1". These values are updated throughout the training process of the model and converted to the representation with the best expression ability. This allows the relationship between the values obtained with text vectorization to be expressed. Furthermore, deep learning algorithms are provided with the opportunity to achieve better performance in each iteration.
 
Once all the requisite steps have been completed, the progress achieved in each phase of the model training process is represented graphically and exported for further analysis. Subsequently, a model file is generated to facilitate the reuse of the trained model. Subsequently, the classification step of the binary file is initiated following the measurement of performance with the test set. In order to perform a classification, the relevant files must first be converted to machine code by decompilation. The machine codes are then converted to decimal values. An input is then generated from these decimal values according to the data format. Classification is then performed using the aforementioned model with the input. Subsequently, the process of cyber threat intelligence creation is initiated upon completion of the classification stage. At this stage, the classification outcome is initially evaluated. In the event that the binary file does not exhibit any indications of vulnerability following the classification process, the flow is terminated. In the event that a vulnerability is identified, cyber threat intelligence is generated in accordance with the specific vulnerability inherent to the pertinent file, the binary code section containing the vulnerability, and the metadata obtained. Subsequently, the file is exported and saved. Finally, the flow is terminated.

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
```

## Notes
- In our study(s), 'OneDNN' was used as an abbreviation for 'One-Dimensional CNN'. Please note that this usage is specific to our study and should not be confused with other meanings of 'OneDNN'.
- For detailed information or any question, please feel free to contact me: arikan.sm@gmail.com
