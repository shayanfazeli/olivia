# OLIVIA: Simplified Public Health-focused Spatio-temporal Monitoring

__Remark__: OLIVIA's website [olivia.cs.ucla.edu](http://olivia.cs.ucla.edu) demos the interface, nonetheless, OLIVIA is currently retired. Nonetheless,
given that the source code and data is available, one should be able to deploy a custom version of it easily.
Additionally, we have been collaborating with the Public Health Department at UCLA in creating the [CDCF-funded](https://www.ccpr.ucla.edu/2021/04/30/dr-chandra-ford-and-colleagues-were-awarded-a-1-7-million-grant-from-the-cdc-foundation-to-conduct-research-on-racism-and-covid-19-crisis-communication/) community-centered surveillance system of [Project ReFOCUS](http://projectrefocus.com).

## Introduction
This repository contains the publicly accessible source code for the [OLIVIA](https://dailybruin.com/2020/05/21/ucla-team-compiles-coronavirus-related-data-creates-statistical-modeling-tool) framework.
OLIVIA is a flask-based, layered, and simplified monitoring platform which allows an easy-to-understand interface
for correlative analysis of public health-focused surveillance data. 

With COVID-19 as its main focus as an example of a
use-case beneficial for public health experts, OLIVIA, combined with [a comprehensive dataset](https://shayanfazeli.github.io/olivia_dataset/Readme.html#introduction) containing a multitude of 
data sources covering different domains (e.g., socio-economic, demographic, other health-related information, employment, census, etc.),
OLIVIA framework provides an intuitive and easy to develop framework to set up a surveillance and monitoring web app, data store,
and analytics engine, quickly and in an efficient manner.

## Usage
OLIVIA is written in the [Flask](https://flask.palletsprojects.com/en/2.2.x/) framework and thus can be run accordingly or using [Gunicorn](https://gunicorn.org/).

## Citation
Please use the following reference for citing this work:

```
@inproceedings{fazeli2021statistical,
  title={Statistical analytics and regional representation learning for covid-19 pandemic understanding},
  author={Fazeli, Shayan and Moatamed, Babak and Sarrafzadeh, Majid},
  booktitle={2021 IEEE 9th International Conference on Healthcare Informatics (ICHI)},
  pages={248--257},
  year={2021},
  organization={IEEE}
}
```