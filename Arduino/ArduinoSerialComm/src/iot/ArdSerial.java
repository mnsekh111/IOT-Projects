/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package iot;

import java.io.DataOutputStream;
import java.net.Socket;

import com.fazecast.jSerialComm.SerialPort;
import com.fazecast.jSerialComm.SerialPortEvent;
import com.fazecast.jSerialComm.SerialPortPacketListener;

import packetizer.SinglePacket2;

/**
 *
 * @author root
 */
class PacketListener implements Runnable, SerialPortPacketListener {

	private IMessenger mess = null;
	private boolean started = false;
	private int counter = 0;
	private String customBuffer = "";
	private static final int KEYSTROKE_BITS = 8;
	private static final int FILE_BITS = 128;
	private static final int KEYSTROKE_PACKET_LENGTH = 32;
	private static final int FILE_PACKET_LENGTH = 152;

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
		// mess.sendMessage("\nReceived data of size: " + newData.length +
		// "\n");

		// Arduino is just sending 0's. Actual data transmission not started
		// mess.sendMessage(""+(char)newData[0]);
		if (started == false) {
			if ((char) newData[0] == '1') {
				customBuffer += "1";
			} else if ((char) newData[0] == '0') {
				customBuffer = "";
			}
			if (customBuffer.length() == 5) {
				customBuffer = "";
				started = true;
			}
		} else { // PC2 has detected the start of the packet

			customBuffer += ((char) newData[0]);
			System.out.println(customBuffer.length());

			if (customBuffer.length() == KEYSTROKE_PACKET_LENGTH) {

				int messageId = Integer.parseInt(customBuffer.substring(0, 8), 2);
				String data = "" + (char) Integer.parseInt(customBuffer.substring(8, 8 + KEYSTROKE_BITS), 2);
				String actualChecksum = customBuffer.substring(8 + KEYSTROKE_BITS, 32);

				if (validChecksum(data, actualChecksum)) {
					mess.sendMessage("\nData - " + data);
					sendAck(messageId, true);
				} else {
					sendAck(messageId, false);
				}

				started = false;
				customBuffer = "";
			}

		}

	}

	private void sendAck(int messageId, boolean success) {
		Socket socket = null;
		DataOutputStream dos = null;
		
		if (success) 
			messageId++;
			
		try {
			socket = new Socket("192.168.0.128", 9000);
			dos = new DataOutputStream(socket.getOutputStream());
			
			dos.writeInt(messageId);
			dos.close();
			socket.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private boolean validChecksum(String data, String actualChecksum) {
		String calculatedChecksum = new String();
		byte[] checksum = CheckSum.checkSum16(data.getBytes());

		for (int i = 1; i >= 0; i--)
			for (int j = 0; j < 8; j++) {
				if (isSet(checksum[i], j))
					calculatedChecksum = "1" + calculatedChecksum;
				else
					calculatedChecksum = "0" + calculatedChecksum;
			}
		return calculatedChecksum.equals(actualChecksum);
	}

	private boolean isSet(byte value, int bit) {
		return (value & (1 << bit)) != 0;
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
		} else {
			mess.sendMessage("\nThe port is already open \n");
		}
	}

	public void stop() {
		if (comPort.isOpen()) {
			comPort.removeDataListener();
			comPort.closePort();
			mess.sendMessage("\nThe port is closed successfully \n");
		} else {
			mess.sendMessage("\nThe port already closed \n");
		}
		deinit();
	}

	private void deinit() {
		instance = null;
	}
}
