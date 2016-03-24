import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

import com.pi4j.io.gpio.GpioController;
import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalOutput;
import com.pi4j.io.gpio.PinState;
import com.pi4j.io.gpio.RaspiPin;

class PC1Handler extends Thread {
	private Socket clientSocket = null;
	private static final int READ_SIZE = 1;

	private GpioController gpio = null;
	private GpioPinDigitalOutput pin = null;

	public PC1Handler(Socket soc) {
		this.clientSocket = soc;
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
		try {
			if (clientSocket != null) {

<<<<<<< HEAD
				byte[] byteArray = new byte[READ_SIZE];

				while (in.read(byteArray) != -1) {
					// System.out.println("Received i :99"+(char)byteArray[0]);
					fout.write(byteArray);
					fout.flush();

				
					for (int i = 0; i < 8; i++) {
						if (isSet(byteArray[0],i)) {
							pin.pulse(1000, true);
							System.out.print("1");
						} else {
							System.out.print("0");
							pin.low();
							try {
								Thread.sleep(1000);
							} catch (InterruptedException e) {
								// TODO Auto-generated catch block
								e.printStackTrace();
							}
						}
					}
				}

				gpio.shutdown();
				in.close();
				fout.close();
=======
				saveFile();

				/*
				 * 
				 * 
				 * Rasberry pi GPIO handling Code goes here
				 * 
				 * 
				 */

>>>>>>> master
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

	/**
	 * Saves File received from PC1
	 * 
	 * @throws FileNotFoundException
	 * @throws IOException
	 */
	private void saveFile() throws FileNotFoundException, IOException {
		File file = new File("samplefile");
		FileOutputStream fout = new FileOutputStream(file);
		BufferedInputStream in = new BufferedInputStream(clientSocket.getInputStream());

		byte[] byteArray = new byte[1024];

		while (in.read(byteArray) != -1) {
			fout.write(byteArray);
		}

		in.close();
		fout.close();
	}
}

class PC2Handler extends Thread {
	private Socket clientSocket = null;

	public PC2Handler(Socket soc) {
		this.clientSocket = soc;
	}

	@Override
	public void run() {
		try {
			if (clientSocket != null) {

				BufferedInputStream in = new BufferedInputStream(clientSocket.getInputStream());
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
	public static final int BUFFER_SIZE = 100;
	public static final String PC1 = "192.168.0.100";
	public static final String PC2 = "192.168.0.200";

	// uncomment the following portion for running this code in Intel Edison
	// "from Eclipse"
	// static {
	// try {
	// System.loadLibrary("mraajava");
	// } catch (UnsatisfiedLinkError e) {
	// System.err
	// .println("Native code library failed to load. See the chapter on Dynamic
	// Linking Problems in the SWIG Java documentation for help.\n"
	// + e);
	// System.exit(1);
	// }
	// }

	public static void main(String[] args) throws Exception {
		int portNum = 9991;
		boolean runforever = true;

		ServerSocket serverSocket = null;
		Socket clientSocket = null;

		try {
			serverSocket = new ServerSocket(portNum);
			
			System.out.println("Listening on port " + portNum);
		} catch (IOException ie) {
			System.err.println("Error listening at port " + portNum + "\n" + ie.getLocalizedMessage());
			System.exit(1);
		}

		while (runforever) {
			try {
				System.out.println("Waiting for Client sockets");
				clientSocket = serverSocket.accept();
				System.out.println("Connection received" + clientSocket.getPort());
			} catch (IOException e) {
				System.err.println("Accept failed.");
				System.exit(1);
			}

<<<<<<< HEAD
			String source = clientSocket.getInetAddress()
					.getCanonicalHostName();
			System.out.println("PCI client connected to " + source);
			if (source.contentEquals("localhost") || source.contentEquals("mns-G551JW")) {
=======
			String source = clientSocket.getInetAddress().getCanonicalHostName();
			// System.out.println(source);
			if (source.contentEquals(PC1)) {
>>>>>>> master
				PC1Handler handler = new PC1Handler(clientSocket);
				handler.start();

			} else if (source.contentEquals(PC2)) {
				PC2Handler handler = new PC2Handler(clientSocket);
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