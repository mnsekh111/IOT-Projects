import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.math.BigInteger;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

import com.pi4j.io.gpio.GpioController;
import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalOutput;
import com.pi4j.io.gpio.PinState;
import com.pi4j.io.gpio.RaspiPin;

class PC1Handler extends Thread {
	private Socket clientSocket = null;
	private static final int KESTROKE_READ_SIZE = 1;
	private static final int FILE_READ_SIZE = 16;
	private int mode;
	private GpioController gpio = null;
	private GpioPinDigitalOutput pin = null;
	

	public PC1Handler(Socket soc,int mode) {
		this.clientSocket = soc;
		this.mode = mode;
		 gpio = GpioFactory.getInstance();
		 pin = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_01, "MyLED",
		 PinState.LOW);
		 pin.setShutdownOptions(true, PinState.LOW);

	}

	private boolean isSet(byte value, int bit) {
		return (value & (1 << bit)) != 0;
	}

	@Override
	public void run() {
		if(mode==1)
			handleKeystrokes();
		else if(mode==2)
			handleFiles();

	}

	private void handleFiles() {
		// TODO Auto-generated method stub
		
	}

	private void handleKeystrokes() {
		try {
			if (clientSocket != null) {
				File file = new File("samplefile");
				FileOutputStream fout = new FileOutputStream(file);
				BufferedInputStream in = new BufferedInputStream(
						clientSocket.getInputStream());

				byte[] byteArray = new byte[KESTROKE_READ_SIZE];
				int messageId = 0;

				while (in.read(byteArray) != -1) {
					fout.write(byteArray);
					fout.flush();
					
					byte[] packet = constructPacket(messageId,byteArray);
					
					handleGPIO(packet);
					
					if(messageId==255)
						messageId = 0;
					else
						messageId++;
				}

				gpio.shutdown();
				in.close();
				fout.close();
				clientSocket.close();
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private byte[] constructPacket(int messageId, byte[] byteArray) {
		//Packet = 1 byte MessageId + Data 
		byte[] packet = new byte[1 + byteArray.length];
		
		packet[0] = BigInteger.valueOf(messageId).byteValue();
		
		for(int i=1;i<byteArray.length;i++) {
			packet[i]= byteArray[i];
		}
		return packet;
	}

	/**
	 * This method will accept bytes, construct packet to be sent and handle GPIO accordingly
	 * @param byteArray
	 */
	private void handleGPIO(byte[] byteArray) {
		pin.pulse(500, true);

		for (int i = 0; i < 8*byteArray.length; i++) {
			if (isSet(byteArray[0],i)) {
				pin.pulse(100, true);
				System.out.print("1");
			} else {
				System.out.print("0");
				pin.low();
				try {
					Thread.sleep(100);
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
		pin.pulse(500, true);
	}
}

class PC2Handler extends Thread {
	private Socket clientSocket = null;
	private int mode;
	public PC2Handler(Socket soc,int mode) {
		this.clientSocket = soc;
		this.mode = mode;
	}

	@Override
	public void run() {
		try {
			if (clientSocket != null) {

				BufferedInputStream in = new BufferedInputStream(
						clientSocket.getInputStream());
				/*
				 * 
				 * 
				 * 
				 * 
				 * ACK parsing from PC2 goes here
				 */

			}

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
}

public class IOTClientServer {

	// uncomment the following portion for running this code in Intel Edison
	// "from Eclipse"
	// static {
	// try {
	// System.loadLibrary("mraajava");
	// } catch (UnsatisfiedLinkError e) {
	// System.err
	// .println("Native code library failed to load. See the chapter on Dynamic Linking Problems in the SWIG Java documentation for help.\n"
	// + e);
	// System.exit(1);
	// }
	// }

	public static void main(String[] args) {
		int portNum = 9991;
		boolean runforever = true;
		ServerSocket serverSocket = null;
		Socket clientSocket = null;
		
		Scanner sc = new Scanner(System.in);
		System.out.println("1. Keystroke listening \n 2. File Transfer :");
		int mode = sc.nextInt();

		try {
			serverSocket = new ServerSocket(portNum);
			
			System.out.println("Listening on port " + portNum);
		} catch (IOException ie) {
			System.err.println("Error listening at port " + portNum + "\n"
					+ ie.getLocalizedMessage());
			System.exit(1);
		}

		while (runforever) {
			try {
				System.out.println("Waiting for Client sockets");
				clientSocket = serverSocket.accept();
			} catch (IOException e) {
				System.err.println("Accept failed.");
				System.exit(1);
			}

			String source = clientSocket.getInetAddress()
					.getCanonicalHostName();
			System.out.println("PCI client connected to " + source);
			if (source.contentEquals("localhost") || source.contentEquals("mns-G551JW") || source.contentEquals("vitellius")) {
				PC1Handler handler = new PC1Handler(clientSocket, mode);
				handler.start();

			} else if (source.contentEquals("pc2-client")) {
				PC2Handler handler = new PC2Handler(clientSocket,mode);
				handler.start();
			}
		}

		try {
			serverSocket.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}