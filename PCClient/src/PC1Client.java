/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
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
		//String serverHostname = new String("127.0.0.1");
		String serverHostname = new String("192.168.43.128");
		int portNum = 9991;

		System.out.println("Attemping to connect to host " + serverHostname
				+ " on port " + portNum + ".");

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
				String userInput = sc.nextLine();
				while (!userInput.contentEquals("!q")) {
					byte[] byteArray = userInput.getBytes();
					out.write(byteArray, 0, byteArray.length);
					out.flush();
					//System.out.print("Done");
					userInput = sc.nextLine();
				}

				System.out
						.println("Message sent successfully to Rasberry pi \n");
			} else if (choice == 2) {
				File file = new File("samplefile");

				if (!file.exists()) {
					file.createNewFile();
					/* Write some dummy data into the file */

					/* Finish */
				}

				byte[] byteArray = new byte[(int) file.length()];
				FileInputStream fis = new FileInputStream(file);
				BufferedInputStream bis = new BufferedInputStream(fis);
				bis.read(byteArray, 0, byteArray.length);
				out.write(byteArray, 0, byteArray.length);
				System.out.println("File sent successfully to Rasberry pi\n");

				fis.close();
				bis.close();

			}
		} catch (IOException e) {
			System.out.println("Read / Write exception\n");
		}

		try {
			sc.close();
			out.close();
			in.close();
			socket.close();
		} catch (IOException ex) {
			Logger.getLogger(PC1Client.class.getName()).log(Level.SEVERE, null,
					ex);
		}
	}
}
