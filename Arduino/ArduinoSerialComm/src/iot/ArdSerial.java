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
public class ArdSerial {

    private static final class PacketListener implements SerialPortPacketListener {

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
    }

    public static void main(String[] args) {
//        SerialPort comPort = SerialPort.getCommPorts()[0];
//        comPort.openPort();
//        comPort.addDataListener(new SerialPortDataListener() {
//            @Override
//            public int getListeningEvents() {
//                return SerialPort.LISTENING_EVENT_DATA_AVAILABLE;
//            }
//
//            @Override
//            public void serialEvent(SerialPortEvent event) {
//                if (event.getEventType() != SerialPort.LISTENING_EVENT_DATA_AVAILABLE) {
//                    return;
//                }
//                byte[] newData = new byte[comPort.bytesAvailable()];
//                int numRead = comPort.readBytes(newData, newData.length);
//                System.out.println("Read " + numRead + " bytes.");
//
//            }
//        });

        SerialPort comPort = SerialPort.getCommPorts()[0];
        comPort.openPort();
        PacketListener listener = new PacketListener();
        comPort.addDataListener(listener);
        try {
            Thread.sleep(5000);
        } catch (Exception e) {
            e.printStackTrace();
        }
        comPort.removeDataListener();
        comPort.closePort();
    }
}
