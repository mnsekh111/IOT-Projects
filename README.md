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

5. (alt) . If step 5 causes some problems, then download the Flash Tool Lite package from                        http://downloadmirror.intel.com/24910/eng/phoneflashtoollite_5.2.4.0_linux_x86_64.deb  (download the latest tool)

    1. Install x86 c++ libs `sudo apt-get install gdebi libncurses5:i386 libstdc++6:i386`  
    2. Install the <code>.deb</code> using gdebi or using Ubuntu software center
    3. <code>(Optional) </code>Navigate into the Mount directory and remove all the old file `rm -rf *` 
    4. Search for "Phone Flash Tool" in your applications and run it.
    5. Select the edison-iotdk-image that was downloaded in step 3 and change the configuration from <em>RNDIS to CDC</em>
    6. Click <b>Start to flash</b>. Disconnect and then reconnect the device and the application will take care of flashing
    

    
    <span style="background-color:red"><u>Setting up a serial terminal on a system with Linux</u></span>
    
    1. Install Screen shell session manager installed, open a new Terminal window. Enter the command: <br />
        `sudo apt-get install screen`
    2. To connect to the board, enter the command (where ttyUSB0 is your connected device):
        `sudo screen /dev/ttyUSB0 115200`
    3. Press `Enter` twice. A login screen is displayed. At the login prompt, type `root` and press `Enter`.
      Press `Enter` when prompted for a password.
    4. 

 

