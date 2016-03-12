import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class IOTClientServer {

	static {
		try {
			System.loadLibrary("mraajava");
		} catch (UnsatisfiedLinkError e) {
			System.err
					.println("Native code library failed to load. See the chapter on Dynamic Linking Problems in the SWIG Java documentation for help.\n"
							+ e);
			System.exit(1);
		}
	}

	public static void main(String[] args) {
		int portNum = 9991;

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

		try {
			clientSocket = serverSocket.accept();
		} catch (IOException e) {
			System.err.println("Accept failed.");
			System.exit(1);
		}

		try {
			PrintWriter out = new PrintWriter(clientSocket.getOutputStream(),
					true);
			BufferedReader in = new BufferedReader(new InputStreamReader(
					clientSocket.getInputStream()));

			String inputLine;

			while ((inputLine = in.readLine()) != null) {
				System.out.println("Server: " + inputLine);
				out.println(inputLine);

				if (inputLine.equals("Bye.")) {
					break;
				}
			}

			out.close();
			in.close();
			clientSocket.close();
			serverSocket.close();

		} catch (IOException ex) {

		}

	}

}