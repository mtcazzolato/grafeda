
# GraF-EDA

  

**Graf-EDA: Graph Features for Exploratory Data Analysis**

**Authors:** Mirela Cazzolato<sup>1,2</sup>, Marco Antonio Gutierrez<sup>2</sup>, Caetano Traina Jr.<sup>1</sup>, Christos Faloutsos<sup>3</sup>, Agma J. M. Traina<sup>1</sup>

**Affiliations:**  <sup>1,2</sup> University of São Paulo (USP), <sup>2</sup> The Heart Institute (InCor) - University of São Paulo (HC-FMUSP), <sup>3</sup> Carnegie Mellon University (CMU)

This work will be presented at the [IEEE 36th International Symposium on Computer Based Medical Systems (CBMS) 2023 - June 22 - 24 - L'Aquila, Italy.](https://2023.cbms-conference.org/) 
 
  
## License Agreement and Citation Request  

*GraF-EDA* is available for researchers and data scientists under the GNU General Public License. In case of publication and/or public use of the available data and code, as well as any resource derived from it, one should acknowledge its creators by citing **the following paper** (the reference will be updated to its definitive version soon).
  
**Published paper, to appear:**

> \[Cazzolato *et al.*, 2022\] CAZZOLATO, M. T.;  GUTIERREZ, M.A.;  TRAINA-JR., C.; FALOUTSOS, C.; TRAINA, A. J. M.. **GraF-EDA: Graph Features for Exploratory Data Analysis.** In the IEEE 36th International Symposium on Computer Based Medical Systems (CBMS), 2023.


## Setup environment

  

To setup and use a virtual environment, type in the Terminal:

  

```

python -m venv grafeda_venv

source grafeda_venv/bin/activate

```

  

Install the requirements:

  

pip install -r requirements.txt

or

  

make prep

  

Run the app:

  

make demo

  
## Demo  

Feature extraction:  


https://github.com/mtcazzolato/grafeda/assets/8514761/a0618f81-9abe-4290-9031-d5a1af401f0c


Feature loading:  



https://github.com/mtcazzolato/grafeda/assets/8514761/c14c59bb-1209-4f62-8109-065e885c009e


EDA of extracted features:  



https://github.com/mtcazzolato/grafeda/assets/8514761/4a4eb2bf-c416-4ed8-ba2c-37fbf8be05a8



## Dataset and Features

The [Covid-19 Data Sharing Repository]([https://repositoriodatasharingfapesp.uspdigital.usp.br/](https://repositoriodatasharingfapesp.uspdigital.usp.br/)) provides Electronic Health Record (EHR) data from hospitals of São Paulo state, Brazil. The EHRs were collected between 2020 and 2021 [1].

Following, we provide the ***features extracted*** and used in our work, for datasets: *Complete*, *ds-BPSP*, *ds-Einstein*, *ds-HC*, *ds-HSL*. For more details, please refer to the paper.

  
  

***Download:***

  

-  **Table Patient**

-  *Attributes:* Patient and Exam: [link](https://drive.google.com/drive/folders/1y2_SDW1AkUwVg64omU6isbVBOc2TSUT8?usp=sharing)

-  **Table: Patient**

-  *Attributes:* Treatment and Exam: [link](https://drive.google.com/drive/folders/1ocjN148UsoFUJejChgAK_BjQ_9YIbABe?usp=sharing)

  

-  **Table: Outcome**

-  *Attributes:* Clinic and Outcome: [link](https://drive.google.com/drive/folders/15Zy1QSMnutFdrgnCp7EOBn25hNYvikWB?usp=sharing)

## References

  

[1] FAPESP. **FAPESP COVID-19 Data Sharing/BR,** Available from [**https://repositoriodatasharingfapesp.uspdigital.usp.br/**](https://repositoriodatasharingfapesp.uspdigital.usp.br/)**.** Accessed on March 10th 2023
