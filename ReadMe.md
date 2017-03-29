Welcome to the home of **Python Tracking Framework (PTF)** - a collection of registration based trackers (like IC, ESM, NN, PF and L1) and related utilities implemented in Python and Cython along with supporting Matlab scripts

Prerequisites:
==============
* [OpenCV](http://opencv.org/)
* [FLANN](http://www.cs.ubc.ca/research/flann/) (optional)
* [Cython](http://cython.org/) (optional)
* [MTF](http://webdocs.cs.ualberta.ca/~vis/mtf/) (optional)
* [Xvision](https://bitbucket.org/abhineet123/xvision2) (optional)
		
Installation
============

All optional Cython and C modules used by PTF can be compiled and installed by simply calling `make` from the root folder. This in turn calls the make commands in the following sub folders: `CModules`, `cython_trackers`, `l1`. 

* It also executes the command to compile and install the Python interface to the [**Modular Tracking Framework**](http://webdocs.cs.ualberta.ca/~vis/mtf/) called `pyMTF`. This requires the source code of this library to be present in `~/mtf` folder.  Change the variable `MTF_DIR` in the makefile if the source code is present elsewhere.  
* If Xvision is not installed, either remove `xv` from the `all` target of the makefile before calling the `make` command or call the following separate commands instead:

    * `make dl`
    * `make cython`
    * `make l1`
    * `make mtf`


Basic Usage
===========
Setting parameters:

Set `db_root_path` in `main.py` if running on dataset sequences and adjust remaining settings in `config.py`.

Running with GUI:
```
python main.py
```
Running without GUI with default parameter settings in `config.py`:
```
python main.py 0
```
