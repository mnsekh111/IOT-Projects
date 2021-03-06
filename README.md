# Arduino specific setup details
https://github.com/mnsekh111/IOT-Projects/tree/master/Arduino/Sketch_Photo_diode

# IOT-Projects

<blockquote>All IOT programming done as part of CSC591</blockquote>

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
    

    
    ###<span style="background-color:red">Setting up a serial terminal on a system with Link</span>
    
    1. Install Screen shell session manager installed, open a new Terminal window. Enter the command: <br />
        `sudo apt-get install screen`
    2. To connect to the board, enter the command (where ttyUSB0 is your connected device):
        `sudo screen /dev/ttyUSB0 115200`
    3. Press `Enter` twice. A login screen is displayed. At the login prompt, type `root` and press `Enter`.
        Press `Enter` when prompted for a password.
    4. Now the root@edison terminal is open.
    
    ###<span style="background-color:red">Setting up Wifi</span>
    
    1. Type `configure_edison --wifi` <br/>If you get an error saying configure_edison: not found, you need to update your         firmware
    2. Follow the steps which are straight forward. Once connected, try opening the ip address where Edison is hosted.
        If unable to access the site, then it means the device is not properly connected to the network.
    3. Change the password of the device using configure_edison --password
    
    other options to look out: <br/>
  <pre> -h, --help            show this help message and exit
  --setup               Goes through changing the device name, password, and
                        wifi options
  --name                Changes the device name
  --password            Changes the device password
  --wifi                Changes the wifi options
  --showWiFiIP          IP address associated with the wireless interface
  --showWiFiMode        Show current mode for the wireless interface
  --version             Gets the current firmware version
  --latest-version      Gets the latest firmware version
  --disableOneTimeSetup
                        Disable one-time setup with WiFi access point and
                        enable WiFi client mode Append --persist to retain
                        this setting after reboot
  --enableOneTimeSetup  Enable one-time setup with WiFi access point and
                        disable WiFi client mode. Append --persist to retain
                        this setting after reboot
  --toggleOneTimeSetup  Switch between one-time setup with WiFi access point
                        and WiFi client mode, and visa-versa. Append --persist
                        to retain this setting after reboot
  --upgrade             Downloads the latest firmware. Append --restartWithAP
                        to reboot in WiFi access point mode after flashing
  --flash <version> [<release name> ...]
                        Downloads and flashes an image Append --restartWithAP
                        to reboot in WiFi access point mode after flashing
  --flashFile <image-file>
                        Flashes the given image (.zip). Append --restartWithAP
                        to reboot WiFi access point mode after flashing
  --showNames           Show device name and SSID
</pre>

<hr/>
#Arduino Uno

####Understanding the anatomy
    https://www.arduino.cc/en/Guide/BoardAnatomy

#### Understanding breadboard (For an electronics noob like me)
    https://www.youtube.com/watch?v=Iy7DY2UbHvM
    
##Setting up wifi in Arduino:
1: Mount the ESP6266 Wifi Shield over the arduino board
2. Learn more about the wifi shield here <br>
    https://learn.sparkfun.com/tutorials/esp8266-wifi-shield-hookup-guide

LED Indicators

The WiFi Shield includes two LED indicators: a simple red power indicator and a blue “status” LED. The red power LED should illuminate whenever power is being delivered from the Arduino to the ESP8266 Shield. If you need to debug anything, checking for this LED should be your first step.

LED indicator location

The blue status LED is tied into the firmware of the ESP8266. It’ll blink, be solid, or turn off depending on which state it’s in.

<table class="table table-striped table-bordered">
<tbody><tr><th>LED State</th><th>ESP8266 State</th></tr>
<tr><td>Off</td><td>WiFi disconnected. Not configured.</td></tr>
<tr><td>Blinking</td><td>Station mode: ESP8266 attempting to connect to access point.<br>AP mode: ESP8266 waiting for incoming connections</td></tr>
<tr><td>On</td><td>Station mode: ESP8266 connected to access point.<br>AP mode: Devices connected to ESP8266 AP.</td></tr>
</tbody></table>
LED State	ESP8266 State
Off	WiFi disconnected. Not configured.
Blinking	Station mode: ESP8266 attempting to connect to access point.
AP mode: ESP8266 waiting for incoming connections
On	Station mode: ESP8266 connected to access point.
AP mode: Devices connected to ESP8266 AP.
The status LED is tied to GPIO 5 of the ESP8266.


###Arduino Serial Comm Set up
1. Download the java rxtx libraray from <br>http://fizzed.com/oss/rxtx-for-java
2. Extract the above zip and do the following <br>
    1. Copy RXTXcomm.jar ---> <JAVA_HOME>/jre/lib/ext
    2. Copy librxtxSerial.so ---> <JAVA_HOME>/jre/lib/amd64/
    3. Copy librxtxParallel.so ---> <JAVA_HOME>/jre/lib/amd64/

3. Go to the following website and download the code <br>
    http://playground.arduino.cc/Interfacing/Java

4. Install an IDE like netbeans and create a Java project and paste the code available in the above mentioned website.
5. (optional) In the <code>project properties</code> under <code>Libraries</code>, add RXTXComm.jar and in <code>Run , VM Options</code> add the location of the jni compatible .so file (Not necessary as you have already pasted that in /jre/lib/amd64)
    -Djava.library.path=/home/mns/Downloads/rxtx-2.1-7-bins-r2/Linux/x86_64-unknown-linux-gnu/librxtxSerial.so

6. <div style="background-color:cyan">Run Netbeans in root mode</div>. Otherwise <code>CommPortIdentifier.getPortIdentifiers();</code> will return empty/null


####Rasberry Pi

Controlling GPIO pins using Java : 
http://pi4j.com/example/control.html


 

