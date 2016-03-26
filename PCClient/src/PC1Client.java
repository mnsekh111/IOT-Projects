
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.Console;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.Reader;
import java.math.BigInteger;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author mns
 */
public class PC1Client {

	public static void main(String[] args) {
		System.out.println("PC Client started");
		String serverHostname;
		serverHostname = new String("192.168.43.128");
		//serverHostname = new String("127.0.0.1");
		int portNum = 9991;

		System.out.println("Attemping to connect to host " + serverHostname + " on port " + portNum + ".");

		Socket socket = null;
		BufferedOutputStream out = null;
		BufferedInputStream in = null;
		int choice;

		try {

			socket = new Socket(serverHostname, portNum);
			out = new BufferedOutputStream(socket.getOutputStream());
			in = new BufferedInputStream(socket.getInputStream());

		} catch (UnknownHostException e) {
			System.err.println("Unknown host " + serverHostname);
			System.exit(1);
		} catch (IOException e) {
			System.err.println("Couldn't connect to " + serverHostname);
			System.exit(1);
		}

		Scanner sc = new Scanner(System.in);
		System.out.println("1. Send a message \n2. Transfer a file \n");
		choice = Integer.parseInt(sc.nextLine());

		try {
			if (choice == 1) {

				System.out.print("Enter Live messages : ");
				String[] cmd = { "/bin/sh", "-c", "stty raw </dev/tty" };
				Runtime.getRuntime().exec(cmd).waitFor();
				Console console = System.console();
				Reader reader = console.reader();

				while (true) {
					int inputAscii = reader.read();

					if (String.valueOf(inputAscii).equalsIgnoreCase("9"))
						break;
					
					byte[] byteArray = BigInteger.valueOf(inputAscii).toByteArray();

					out.write(byteArray, 0, byteArray.length); 
					out.flush();

					System.out.println("input Ascii - " + inputAscii);
					for(byte b:byteArray)
						System.out.println("bytes - "+b);

				}
				cmd = new String[] { "/bin/sh", "-c", "stty sane </dev/tty" };
				Runtime.getRuntime().exec(cmd).waitFor();
			} else if (choice == 2) {
				System.out.println("Enter the name of the file :");
				Scanner scanner = new Scanner(System.in);
				String fileName = scanner.nextLine();
				//String fileName = "/tmp/test";
				
				File file = new File(fileName);
				
				byte[] byteArray = new byte[(int) file.length()];
				FileInputStream fis = new FileInputStream(file);
				BufferedInputStream bis = new BufferedInputStream(fis);
				bis.read(byteArray, 0, byteArray.length);
				out.write(byteArray, 0, byteArray.length);
				System.out.println("File sent successfully to Rasberry pi\n");

				fis.close();
				bis.close();

			}
		} catch (Exception e) {
			System.out.println("Read / Write exception\n" + e.getMessage());
		}

		try {
			sc.close();
			out.close();
			in.close();
			socket.close();
		} catch (IOException ex) {
			Logger.getLogger(PC1Client.class.getName()).log(Level.SEVERE, null, ex);
		}
	}

}
