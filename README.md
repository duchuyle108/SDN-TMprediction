# Introduction

This project represents the work in our paper submmitted to IEEE International Conference on Communications 2021 **"An AI-based Traffic Matrix Prediction Solution for Software-Defined Network"** - Authors: **Duc-Huy LE, Hai Anh TRAN, Sami SOUIHI, Abdelhamid MELLOUK**

In this project, we provide:
- SDN application source codes
- Our Testbed configuration, deployment including scripts and used resources
- Two TM datasets
- Model training and evaluation source codes

Every above component is described in this README.

# Dependencies

## POX controller
We use [POX](https://github.com/noxrepo/pox) to deploy our management and monitoring SDN application. POX can work in any OS Environment that support python 2. You can install pox as following:

```bash
git clone http://github.com/noxrepo/pox
```

## Mininet
To simulate an SDN network, we use the popular framework [Mininet](http://mininet.org/). Mininet currenttly only works in Linux. In our project, we run mininet in an Ubuntu LTS 18.04 VM. To get mininet, you can simply download a compressed Mininet VM from [Mininet downloadpage](https://github.com/mininet/mininet/wiki/Mininet-VM-Images) or install through apt:

```bash
sudo apt update
sudo apt install mininet
```

or install natively from source:
```bash
git clone git://github.com/mininet/mininet
cd mininet
git tag  # list available versions
git checkout -b cs244-spring-2012-final  # or whatever version you wish to install
util/install.sh -a
```

## Machine Learning packages

In our project, we use [keras](https://keras.io/) and tensorflow framework to train our models, in addition, we also use several packages such as **pandas**, **numpy**, **sklearn** to preprocess data for training and **matplotlib** for result visualization. All ML source codes are written in **jupyter-notebook**. The packages can be installed by **pip** as follows:

```bash
python -m pip install -U pip
python -m pip install tensorflow, keras, numpy, pandas, scikit-learn, matplotlib, jupyter-notebook
```
## Testbed auxiliary components

In our custom testbed, to generate traffic in our simulated network, we use **tcpreplay** to emulate packets from network capture files (.pcap). Before that, we use several components(**tcprewrite**, **bittwiste**, **editcap**, **mergecap**) to modify the files so that they can fit the hosts's identity. 


# Acknowledment

This research is funded by Vietnam National Foundation for Science and Technology Development (NAFOSTED)