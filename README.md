
# GraF-EDA

**Graf-EDA: Graph Features for Exploratory Data Analysis**  
**Authors:** Mirela Cazzolato<sup>1,2</sup>, Marco Antonio Gutierrez<sup>2</sup>, Caetano Traina Jr.<sup>1</sup>, Christos Faloutsos<sup>3</sup>, Agma J. M. Traina<sup>1</sup>
**Affiliations:**  <sup>1,2</sup> University of São Paulo (USP), <sup>2</sup> The Heart Institute (InCor) - University of São Paulo (HC-FMUSP), <sup>3</sup> Carnegie Mellon University (CMU)
   
*Work under review.*

## Setup environment

To setup and use a virtual environment, type in the Terminal:

```
python -m venv tgrapp_venv  
source tgrapp_venv/bin/activate  
```

Install the requirements:

    pip install -r requirements.txt
 or

    make prep

Run the app:

    make demo


## Dataset  and Features
  
The [Covid-19 Data Sharing Repository]([https://repositoriodatasharingfapesp.uspdigital.usp.br/](https://repositoriodatasharingfapesp.uspdigital.usp.br/)) provides Electronic Health Record (EHR) data from hospitals of São Paulo state, Brazil. The EHRs were collected between 2020 and 2021 [1].  
Following, we provide the ***features extracted*** and used in our work, for datasets: *Complete*, *ds-BPSP*,  *ds-Einstein*, *ds-HC*, *ds-HSL*. For more details, please refer to the paper.


| Table| Attributes | Download | 
|--|--|--|--|  
| Patient | Patient and Exam   | [link](https://drive.google.com/drive/folders/1y2_SDW1AkUwVg64omU6isbVBOc2TSUT8?usp=sharing) |  
| Patient | Treatment and Exam | [link](https://drive.google.com/drive/folders/1ocjN148UsoFUJejChgAK_BjQ_9YIbABe?usp=sharing) |  
| Outcome | Clinic and Outcome | [link](https://drive.google.com/drive/folders/15Zy1QSMnutFdrgnCp7EOBn25hNYvikWB?usp=sharing) |  
  
## References

[1] FAPESP.  **FAPESP COVID-19 Data Sharing/BR,** Available from [**https://repositoriodatasharingfapesp.uspdigital.usp.br/**](https://repositoriodatasharingfapesp.uspdigital.usp.br/)**.** Accessed on March 10th 2023
