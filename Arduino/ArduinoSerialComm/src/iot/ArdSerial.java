/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package iot;

import packetizer.SinglePacket2;
import com.fazecast.jSerialComm.*;
import java.util.ArrayList;

/**
 *
 * @author root
 */
class PacketListener implements Runnable, SerialPortPacketListener {

    private IMessenger mess = null;
    private boolean started = false;
    private int counter = 0;
    private String customBuffer = "";
    
    public PacketListener(IMessenger imes) {
        this.mess = imes;
    }

    @Override
    public int getListeningEvents() {
        return SerialPort.LISTENING_EVENT_DATA_RECEIVED;
    }

    @Override
    public int getPacketSize() {
        return 1;
    }

    @Override
    public void serialEvent(SerialPortEvent event) {
        byte[] newData = event.getReceivedData();
        //mess.sendMessage("\nReceived data of size: " + newData.length + "\n");
           
        //Arduino is just sending 0's. Actual data transmission not started
        //mess.sendMessage(""+(char)newData[0]);
        if(started == false){
            if((char)newData[0] == '1'){
                customBuffer+="1";
            }else if((char)newData[0]=='0'){
                customBuffer="";
            }
            if(customBuffer.length() == 5){
                customBuffer="";
                started = true;
            }
        }else{  //PC2 has detected the start of the packet
            
            customBuffer+=((char)newData[0]);
            System.out.println(customBuffer.length());
            
            //Message id received
            if(customBuffer.length() == 8){         
                //mess.sendMessage(""+(char)Integer.parseInt(customBuffer.substring(0,8),2));
            }
            
            //Message payload received
            else if(customBuffer.length() == 16){
                mess.sendMessage(""+(char)Integer.parseInt(customBuffer.substring(8,16),2) + " "+customBuffer.substring(8,16)+"\n");
                started = false;
                customBuffer="";
            }
            
        }
        
    }

    @Override
    public void run() {

    }
}

public class ArdSerial {

    private static ArdSerial instance = null;
    private IMessenger mess = null;
    private SerialPort comPort;
    private PacketListener listener = null;

    private ArdSerial(IMessenger imes) {
        comPort = SerialPort.getCommPorts()[0];
        listener = new PacketListener(imes);
        mess = imes;
    }

    public static ArdSerial getInstance(IMessenger imes) {
        if (instance == null) {
            return new ArdSerial(imes);
        }
        return instance;
    }

    public void start() {

        if (!comPort.isOpen()) {
            comPort.openPort();
            comPort.addDataListener(listener);
             mess.sendMessage("\nThe port is opened successfully ! \n");
             SinglePacket2.initSinglePacket(0, 0, 0, 7, 7, 7);
        }else{
            mess.sendMessage("\nThe port is already open \n");
        }
    }

    public void stop() {
        if (comPort.isOpen()) {
            comPort.removeDataListener();
            comPort.closePort();
             mess.sendMessage("\nThe port is closed successfully \n");
        }else{
            mess.sendMessage("\nThe port already closed \n");
        }
        deinit();
    }

    private void deinit() {
        instance = null;
    }
}
