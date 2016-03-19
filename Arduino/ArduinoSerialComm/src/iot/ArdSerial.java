/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package iot;

import com.fazecast.jSerialComm.*;

/**
 *
 * @author root
 */
class PacketListener implements Runnable, SerialPortPacketListener {

    @Override
    public int getListeningEvents() {
        return SerialPort.LISTENING_EVENT_DATA_RECEIVED;
    }

    @Override
    public int getPacketSize() {
        return 100;
    }

    @Override
    public void serialEvent(SerialPortEvent event) {
        byte[] newData = event.getReceivedData();
        System.out.println("Received data of size: " + newData.length);
        for (int i = 0; i < newData.length; ++i) {
            System.out.print((char) newData[i]);
        }
        System.out.println("\n");
    }

    @Override
    public void run() {

    }
}

public class ArdSerial {

    private static ArdSerial instance = null;
    private SerialPort comPort;
    private PacketListener listener = null;

    private ArdSerial() {
        comPort = SerialPort.getCommPorts()[0];
        listener = new PacketListener();

    }

    public static ArdSerial getInstance(){
        if(instance == null){
            return new ArdSerial();
        }
        return instance;
    }
    
    public void start() {

        if (!comPort.isOpen()) {
            comPort.openPort();
            comPort.addDataListener(listener);
        }
    }

    public void stop() {
        if (comPort.isOpen()) {
            comPort.removeDataListener();
            comPort.closePort();
        }
        deinit();
    }
    
    private void deinit(){
        instance = null;
    }
}
