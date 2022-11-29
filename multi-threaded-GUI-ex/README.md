## Multi-Threaded GUI Example
  
### Description
  
This directory contains a simple example of the performance difference between a single-threaded GUI and a multi-threaded GUI that must complete a long-running task (i.e. sleeping)

### Dependencies

1. Python3
2. PyQt5

### Instructions

The two versions of the GUI can be run using one of the following two commands:
```bash
python3 main-single-thread.py
python3 main-multi-thread.py
```

After running either version, enjoy observing the GUI response after pressing the "Long-Running Task" button. :)

### References

In addition to the existing AdiPress Gen II GUI software, this code was developed using official Qt [documentation](https://doc.qt.io/qtforpython-5/), this Real Python [example](https://realpython.com/python-pyqt-qthread/), and this [third-party source](https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html) regarding signals and slots.

### Licenses

All rights reserved by Parker Isaac Instruments.
