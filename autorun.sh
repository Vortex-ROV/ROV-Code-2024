# !bin/bash
export OPENBLAS_CORETYPE=ARMV8
export PYTHONPATH=/home/rov/.local/lib/python3.6/site-packages
export PATH="${PATH}:/home/rov/.local/bin"
/usr/bin/python3.6 /home/rov/ROV-Code/main.py &
/usr/bin/python3.6 /home/rov/.local/bin/mavproxy.py --master /dev/ttyACM0 --out 192.168.33.100:14550 --daemon
