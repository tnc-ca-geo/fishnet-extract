# extract

Simple Python tool to extract images from videos. Currently supports only one annotation file format.

## Instruction for use on Windows

### Install Python 2.7

We are using Python 2.7 because of its ubiquity and possible compatibility
issues in some of the modules used.

Test whether Python is installed on your system path:

Go to start menu > type ```cmd``` into search field > open cmd

Type ```python -V``` on the command line. It should return something like:

```Python 2.7.9```

It has to be 2.7., ideally newer than 2.7.8.

If this command informs you that it did not find a Python executable, get Python for Windows here 
https://www.python.org/downloads/ and install Python 2.7 (NOT 3.x).

Once you install Python it may require that you add it to the windows path env variable, do this in the command line by typing

```setx path "%path%;C:\Python27;C:\Python27\Scripts;"```

you'll need to close and re-open your cmd window after you do this in order for it to take effect

### Test whether pip is available

Pip is Python's package manager. Since Python 2.7.9 it ships with the install and should be readily available.

Try: ```pip --help```

If that fails, you might

1. update the window path env variable for pip using ```setx path "%path%;C:\Python27\Scripts;"```

2. Update your Python installation

3. Get pip separately, see here https://www.python.org/downloads/

### Get this repository 

Either download [zip file](https://codeload.github.com/tnc-ca-geo/extract/zip/master) or use 
```git clone https://github.com/tnc-ca-geo/extract.git``` if you are familar with git and have it installed on your system.

If you downloaded the zip file, unpack it and place it somewhere easy to find like ```C:\extract-master```

### Install dependencies

Find the requirements.txt file in ```C:\extract-master```. Open ```cmd``` or use the already open terminal. Navigate ```cd``` to the folder where requirements.txt is situated. Then type:

```pip install -r requirements.txt```

This will install the dependencies globally on the system, there are number of non-python libraries that will be installed if not already installed. You might run into permission issues. In this case you should run


a) ```cmd``` with administrator privileges and try again

b) try to use isolated virtual environments for installation (directions see below).


### Run the script

Use your ```cmd``` terminal to make sure all the modules are installed properly. Go to C:\extract-master and type:

```python extract.py --help```

These scripts rely on https://ffmpeg.org/ and this will be automatically downloaded after running help if you do not have it

If you have several versions of Python installed on your system, you might provide an explicit path to python 2.7.9 or above, e.g.

```C:\Python27\python extract.py --help```

If you use a virtual env make sure it is activated (see below).

The output of above command should look like this (which also provides the directions for use):

```
extract.py --videofile <inputfile> --annotations <annotationfile>.txt

options:
          -o --offset  Start time of the video (you might be able to get it from the first frame).
                       If not provided, EXIF 'Create Date' will be used.
                       Time format is "YYYY-MM-DD HH:MM:SS". 
                       Use quotes around the date or escape otherwise.
          -f --folder  Output folder. If not provided the current folder will be used.
          -w --window  Number of seconds that will be extracted from the event start. Defaults to 3.
          -h --help    This help
```

Example (assuming media files sitting in ```C:\media``` folder next to the script folder:

```
python extract.py -v C:\media\cam_3_day.mp4 -a C:\media\1631.txt -o "2016-08-14 05:31:18" -f C:\media\stills
```
where:
cam_3_day.mp4 = example name of input video file, file name should not include spaces

1631.txt = Input annotations text file. We are using AnnotationDateTime to specify extract location, please ensure a replacement file looks identical (e.g. AnnotationDateTime in same column position)

Notes:

- Script can handle relative and absolute file names
- videofile and csv of annotations are required
- without an output path images will be stored in the ```extract-master``` folder (not ideal)
- output folder will NOT be created by script, please create manually,the above example uses a folder called "stills"
- during the first run moviepy will acquire [ffmpeg](https://www.ffmpeg.org/) if not avialable on your system, you might be able to install manually if that step fails.

### Appendix: Use with virtualenv

Virtualenv is a way to isolate application dependencies for python.

If you want to use virtualenv to protect other Python dependencies or you do not have privileges to install sytem-wide Python packages. You can create a virtualenv by typing.

```
virtualenv env
``` 

If you have several versions of Pythons on the system it will use the one on your system path (or the one ```which python```) returns. Use the -p flag to point to a different python executable if necessary.

A good place to create this environment would be inside or next to the script folder but it does not really matter as long as this environment is activate.

The command will create a env folder which will contain a copy of the Python executable, the Python modules, as well as scripts to activate or deactivate the virtualenv. 

Activate:

```
env\Scripts\activate.bat
```

Deactivate

```
env\Scripts\deactivate.bat
```

If you use the virtualenv, you have to activate BEFORE you run pip install. Pip install will install in whatever environment is active.
