This chapter requires Scapy from https://scapy.net/
works best on linux machines.

Install OpenCV libraries:
1. `apt-get install libopencv-dev python3-opencv python3-numpy python3-scipy`
Get facial detection training file
1. `wget http://eclecti.cc/files/2008/03/haarcascade_frontalface_alt.xml`
2. `cp haarcascade_frontalface_alt.xml /root/Desktop/training`

setup environment for images
1. `mkdir /root/Desktop/pictures`
2. `mkdir /root/Desktop/faces`
