import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

class PC1Handler extends Thread {
	private Socket clientSocket = null;

	public PC1Handler(Socket soc) {
		this.clientSocket = soc;
	}

	@Override
	public void run() {
		try {
			if (clientSocket != null) {
				File file = new File("samplefile");
				FileOutputStream fout = new FileOutputStream(file);
				BufferedInputStream in = new BufferedInputStream(
						clientSocket.getInputStream());

				byte[] byteArray = new byte[1024];

				while (in.read(byteArray) != -1) {
					fout.write(byteArray);
				}

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

				BufferedInputStream in = new BufferedInputStream(
						clientSocket.getInputStream());

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
				clientSocket = serverSocket.accept();
			} catch (IOException e) {
				System.err.println("Accept failed.");
				System.exit(1);
			}

			String source = clientSocket.getInetAddress()
					.getCanonicalHostName();
			// System.out.println(source);
			if (source.contentEquals("pc1-client")) {
				PC1Handler handler = new PC1Handler(clientSocket);
				handler.start();

			} else if (source.contentEquals("pc2-client")) {
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