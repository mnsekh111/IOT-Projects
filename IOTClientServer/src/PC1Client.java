import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Scanner;

public class PC1Client {
	public static void main(String[] args) throws Exception {
		String fileName = null;
		BufferedInputStream bis = null;
		OutputStream os = null;
		Socket socket = null;

		try {
			System.out.println("Enter the name of the file :");
			Scanner scanner = new Scanner(System.in);
			fileName = scanner.nextLine();

			File file = new File(fileName);
			socket = new Socket("192.168.0.128", 9991);

			byte[] mybytearray = new byte[(int) file.length()];
			bis = new BufferedInputStream(new FileInputStream(file));
			bis.read(mybytearray, 0, mybytearray.length);
			os = socket.getOutputStream();

			System.out.println("Sending " + fileName + "(" + mybytearray.length + " bytes)");
			os.write(mybytearray, 0, mybytearray.length);
			os.flush();
			System.out.println("Done.");

		} catch (Exception e) {
			System.out.println(e.getMessage());
		} finally {
			if (bis != null)
				bis.close();
			if (os != null)
				os.close();
			if (socket != null)
				socket.close();
		}

	}

}