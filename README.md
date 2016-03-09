# IOT-Projects

<blockquote>All IOT programming done as part of CSC592</blockquote>

Setting up Intel Edison on Linux (Ubuntu 14.04.3 Gnome)

1. Follow the steps provided in the below link to assemble intel edison and mount it on your computer
    https://software.intel.com/en-us/articles/assemble-the-intel-edison-board-with-the-mini-breakout-board

2. Open a Terminal window. To install dfu-util, which is an open source program that implements the USB DFU (USB Device         Firmware Upgrade) protocol, enter the command: <br />
    `sudo apt-get install dfu-util`

3. Download the pre-built Yocto* complete image for your board. You can find the most recent version available on the main        downloads page: <br />https://software.intel.com/iot/hardware/edison/downloads <br />e.g http://downloadmirror.intel.com/25384/eng/edison-iotdk-image-280915.zip

4. Extract the zip ( run `sudo apt-get install p7zip-full` if you don't have plugins)

5. Navigate into the extracted folder and enter the command to start flashing the device <br />

    `./flashall.sh`
    (If the process doesn't initialte try to disconnect and remount the device). The flashing process might take 2 to 3          minutes)
    
6. 

