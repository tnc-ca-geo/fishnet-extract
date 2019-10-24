# extract

Extract images from video according to annotation file

```
python extract.py --video_directory <video_directory> --annotations <annotation_file>

options:

   -a --annotations       Annotation file (csv, required)
   -c --crop              Numbers of pixels to crop from top (default 50)
   -f --fps               Extracted frame rate per second (default 5)
   -o --offset            Windows offset from event start in seconds(default -10)
   -s --stills_directory  Output directory (default ./stills/)
   -v --video_directory   Video directory (required)
   -w --window            Extracted window in seconds (default 20)

The annotation csv must implement following columns:

filename ... name of the videofile in which event can be found
start ... start timestamp of the videofile
event ... event timestamp
label ... event label

Edit config.mapping to map an annotation file with different columns names
```

This script required Python 3.6 or higher.

Install dependencies with 
```pip3 install -r requirements.txt```

Activate the virtual environment
```source ~/scripts/env3/bin/activate```

And finally here's an example
```
$ python extract.py -v /home/devuser/data/AFMA/AUCF03-012029-181111_202044/videos -a /home/devuser/data/AFMA/AUCF03-012029-181111_202044/AUCF03-12029_labels_v010.csv -s /home/devuser/data/AFMA/test_stills -o -10 -w 20 -f 3

```
