/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package iot;

import packetizer.SinglePacket2;
import com.fazecast.jSerialComm.*;

/**
 *
 * @author root
 */
class PacketListener implements Runnable, SerialPortPacketListener {

    private IMessenger mess = null;
    public PacketListener(IMessenger imes) {
        this.mess = imes;
    }

    @Override
    public int getListeningEvents() {
        return SerialPort.LISTENING_EVENT_DATA_RECEIVED;
    }

    @Override
    public int getPacketSize() {
        return (SinglePacket2.frame_num_end+1)/8;
    }

    @Override
    public void serialEvent(SerialPortEvent event) {
        byte[] newData = event.getReceivedData();
        //mess.sendMessage("\nReceived data of size: " + newData.length + "\n");
        for (int i = 0; i < newData.length; ++i) {
            mess.sendMessage("" + (char) newData[i]);
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
        }else{
            mess.sendMessage("\nThe port is already open \n");
            SinglePacket2.initSinglePacket(0, 0, 0, 7, 7, 7);
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
