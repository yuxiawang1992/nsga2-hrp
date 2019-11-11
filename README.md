# NSGA-II for hospital relocation problem
Implementation of Non‐dominated Sorting Genetic Algorithm II(NSGA-II) for solving hospital relocation problem (HPR). The code is based on https://github.com/wreszelewski/nsga2

## Reference 
[Optimizing the spatial relocation of hospitals to reduce urban traffic congestion: A case study of Beijing.](https://doi.org/10.1111/tgis.12524) <br>
Wang Yuxia, Tong Daoqin, Li Weimin, Liu Yu, 2019. Transactions in GIS, 23(2):365–386.

## Description
### Motivation
Traffic congestion represents an ongoing serious issue in many large cities. Many public facilities, such as hospitals, tend to be centrally located to ensure they are most accessible to local residents; as a result, they may contribute significantly to a city's traffic congestion. In this study, a multi‐objective spatial optimization model was provided to help formulate hospital relocation plans, taking into account both traffic congestion and hospital accessibility. 
### Implementation
Using intra‐urban movement data, we proposed a method to estimate the area‐wide traffic congestion caused by hospital visits and to identify potential hospitals to be relocated. An NSGA‐II (Non‐dominated Sorting Genetic Algorithm II) algorithm was applied to solve the hospital relocation optimization problem; we applied our model to study optimal hospital relocation plans in Beijing. 
### Results
Analysis results provide a tradeoff between traffic congestion relief and hospital accessibility. We discussed plans that significantly reduce traffic congestion while maintaining a high level of hospital accessibility. Our study has significant policy implications and provides insights for future facility planning and transportation planning.

## Environment
Python Version: 2.7

## Example
Methodology

![][/results/Methodology.png width="300" ]

<img src= "/results/Methodology.png" width="300" >

Hospital Service Area and Relocation Strategy

<img src= "/results/Hospital Service Area-PEK.jpg" width="300" >
<img src= "/results/relocation_strategy.jpg" width="300" >




