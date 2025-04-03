# Federated Learning and Network Security: Foundations, Potential, and Resilience

> [!IMPORTANT]
> Note: The repository currently hosts the existing materials from ICDCS 2024 as reference, but its content is being updated for the 2025 edition.

This tutorial will be held at the [45th IEEE International Conference on Distributed Computing Systems](https://icdcs2025.icdcs.org/) (ICDCS 2025) in July 2025.
This repository contains the materials, including the Jupyter notebooks and the presentations support, that have been used during the tutorial.
You can find a published summary of the tutorial content in the conference proceedings.


## Abstract

Federated Learning (FL) is a Machine Learning paradigm that enables training models across distributed clients without accessing their data.
In the context of network security, FL can be used to collaboratively train Intrusion Detection System (IDS) models across multiple organizations, virtually extending the local dataset of each participant.
Among the new challenges raised by this approach, the heterogeneity of the clients’ environments induce consequent differences in the data distributions, and therefore contributions.
Further, identifying and mitigating malicious contributions is made more complex in heterogeneous environments.

This tutorial introduces the audience to the principles of FL and its application to network security, and more specifically to build Collaborative Intrusion Detection Systems (CIDSs) using FL.
We address open challenges on that regard, before focusing on the problem of training on heterogeneous data.
Finally, we discuss the issues raised by using FL in the context of network security, with a particular focus on poisoning attacks.


## Speakers

### Yann Busnel

<p align="center">
    <img src="./img/yann.png" alt="Yann Busnel - ICDCS 2025" style="width: 50%; max-width: 200px;">
</p>

Yann Busnel is Senior Vice-President for Research at the Institut Mines-Télécom (IMT), France.
With several years of experience within the IMT group, particularly at IMT Atlantique and IMT Nord Europe, he is responsible for developing and implementing the institution’s scientific strategy.
His work involves fostering inter-affiliate collaborations, overseeing doctoral programs, managing the PhD diploma of IMT, and coordinating the activities of its 11 scientific communities.

He has over 15 years of experience in research and higher education.
Between June 2023 and September 2024, he served as Director of Research and Innovation at IMT Nord Europe.
Before that, he has held various academic positions and responsibilities in France and abroad: Full Professor at IMT Atlantique, Associate Professor at ENSAI in Rennes, Assistant Professor the University of Nantes, and Sapienza University of Rome.

His research topics are mainly related to Models for large-scale distributed systems and networks, with application in Data stream analysis, Cybersecurity, Massive health data and Artificial Intelligence. Recently, his areas of application range from (1) cybersecurity and dependability to (2) the analysis of medical data, in the context of pharmacovigilance or genomic sequence analysis, and (3) the self-organized coordination of fleets of drones. He has published over 100 articles in peer-reviewed journals and conferences. He has also coordinated several national and international collaborative research projects, and is currently a member of the steering committee of the French national research group on networks and distributed systems (GDR RSD).


### Léo Lavaur

<p align="center">
    <img src="./img/leo.png" alt="Leo Lavaur - ICDCS 2025" style="width: 50%; max-width: 200px;">
</p>

Léo Lavaur is a Postdoctoral Researcher at the Interdisciplinary Centre for Security, Reliability and Trust (SnT), University of Luxembourg.
He received his Ph.D. in cybersecurity from IMT Atlantique, France, in 2024, where he focused on applying Federated Learning to Collaborative Intrusion Detection.
During his Ph.D., he collaborated closely with the Chair on Cybersecurity in Critical Networked Infrastructures (Cyber CNI) and its industrial partners, who partially funded his research.
He holds an Engineering degree in Information Security from ENSIBS, Vannes, France. During his studies, he also worked part-time at Orange Cyberdefense.

His research explores various aspects of distributed system security, with a particular emphasis on collaborative knowledge sharing through machine learning.
His contributions range from applying Federated Learning to network security to ensuring the security of FL architectures themselves.
He also has ongoing research activities on dataset generation, model evaluation, and data-quality challenges in FL, as well as communication-efficient decentralized learning.
He currently focuses on modeling causal dependencies in distributed microservice and GenAI architectures.


## Tutorial content

1. Fundamentals of FL,
2. FL for collaborative security,
3. security of FL architectures.

**Fundamentals of FL.** 
The first lecture introduces the audience to the core principles of FL with examples of applications.
In the hands-on, participants will be introduced to [Flower](https://flower.ai/), an open-source framework for FL in Python, and to existing datasets for FL.
The goal is to lay down the foundations for the rest of the tutorial.

**FL for collaborative security.**
The second lecture will focus on the application of FL to network security, and more specifically to the training of Collaborative Intrusion Detection Systems (CIDS) models.
This part will focus on the challenges raised by the heterogeneity of the clients' environments, and how to address them.
The hands-on will consist of building a simple CIDS model using Flower and a dataset of network traffic, and experiment some of these challenges with toy examples.

**Security in collaborative FL.** 
The last lecture will address some challenges of deploying and running Federated Intrusion Detection Systems (FIDSs).
Depending on the nature of the federation (public or private, trustworthiness of the participants, *etc.*), such systems can be vulnerable to various attacks.
In particular, we will focus on poisoning attacks, where a participant tries to degrade the global model by sending malicious contributions, before discussing possible countermeasures.
The hands-on will consist of simulating a poisoning attack on the CIDS model built in the previous part, and experimenting with strategies to detect and mitigate such attacks.


## Materials

### Installation

The project uses [Poetry](https://python-poetry.org) for Python dependencies management, and [Nix](https://nixos.org) for system dependencies management.

If you are a Nix user, the easiest way to install the dependencies is to use the provided `flake.nix` file, which will create a virtual environment with all the necessary dependencies, including the Python ones.
To do so, simply run the following command from anywhere inside the repository, and open the Jupyter notebooks from the generated shell session.
```bash
nix develop
```

If you are not a Nix user, you can still use Poetry to install the Python dependencies.
To do so, run the following command at the root of the respository.
```bash
poetry install
```
You can then use the genserated virtual environment to run the notebooks.
If not, you can open a shell session using `poetry shell` and run `jupyter notebook` from there.


