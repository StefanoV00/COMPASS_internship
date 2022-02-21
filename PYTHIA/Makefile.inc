# PYTHIA configuration file.
# Generated on ven 20 ago 2021, 19:03:14, CEST with the user supplied options:
# --with-root=/home/stefano/root
# --with-python
# --with-lhapdf6=/home/stefano/lhapdf6

# Install directory prefixes.
PREFIX_BIN=/home/stefano/pythia8306/bin
PREFIX_INCLUDE=/home/stefano/pythia8306/include
PREFIX_LIB=/home/stefano/pythia8306/lib
PREFIX_SHARE=/home/stefano/pythia8306/share/Pythia8

# Compilation flags (see ./configure --help for further documentation).
CXX=g++
CXX_COMMON=-O2 -std=c++11 -pedantic -W -Wall -Wshadow -fPIC
CXX_SHARED=-shared
CXX_SONAME=-Wl,-soname,
LIB_SUFFIX=.so
OBJ_COMMON=

EVTGEN_USE=false
EVTGEN_CONFIG=
EVTGEN_BIN=
EVTGEN_INCLUDE=
EVTGEN_LIB=

FASTJET3_USE=false
FASTJET3_CONFIG=
FASTJET3_BIN=
FASTJET3_INCLUDE=
FASTJET3_LIB=

HEPMC2_USE=false
HEPMC2_CONFIG=
HEPMC2_BIN=
HEPMC2_INCLUDE=
HEPMC2_LIB=

HEPMC3_USE=false
HEPMC3_CONFIG=
HEPMC3_BIN=
HEPMC3_INCLUDE=
HEPMC3_LIB=

LHAPDF5_USE=false
LHAPDF5_CONFIG=
LHAPDF5_BIN=
LHAPDF5_INCLUDE=
LHAPDF5_LIB=

LHAPDF6_USE=true
LHAPDF6_CONFIG=lhapdf-config
LHAPDF6_BIN=/home/stefano/lhapdf6/bin/
LHAPDF6_INCLUDE=-I/home/stefano/lhapdf6/include
LHAPDF6_LIB=-L/home/stefano/lhapdf6/lib -Wl,-rpath,/home/stefano/lhapdf6/lib -lLHAPDF

POWHEG_USE=false
POWHEG_CONFIG=
POWHEG_BIN=
POWHEG_INCLUDE=
POWHEG_LIB=

RIVET_USE=false
RIVET_CONFIG=
RIVET_BIN=
RIVET_INCLUDE=
RIVET_LIB=

ROOT_USE=true
ROOT_CONFIG=root-config
ROOT_BIN=/home/stefano/root/bin/
ROOT_INCLUDE=-I/home/stefano/root/include
ROOT_LIB=-L/home/stefano/root/lib -Wl,-rpath,/home/stefano/root/lib -lCore

GZIP_USE=false
GZIP_CONFIG=
GZIP_BIN=
GZIP_INCLUDE=
GZIP_LIB=

PYTHON_USE=true
PYTHON_CONFIG=python-config
PYTHON_BIN=
PYTHON_INCLUDE=-I/usr/include/python2.7 -I/usr/include/x86_64-linux-gnu/python2.7
PYTHON_LIB=

MG5MES_USE=false
MG5MES_CONFIG=
MG5MES_BIN=
MG5MES_INCLUDE=
MG5MES_LIB=

OPENMP_USE=false
OPENMP_CONFIG=
OPENMP_BIN=
OPENMP_INCLUDE=
OPENMP_LIB=

MPICH_USE=false
MPICH_CONFIG=
MPICH_BIN=
MPICH_INCLUDE=
MPICH_LIB=

HDF5_USE=false
HDF5_CONFIG=
HDF5_BIN=
HDF5_INCLUDE=
HDF5_LIB=

HIGHFIVE_USE=false
HIGHFIVE_CONFIG=
HIGHFIVE_BIN=
HIGHFIVE_INCLUDE=
HIGHFIVE_LIB=
