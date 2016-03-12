/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author mns
 */
public class EchoClient {

    public static void main(String[] args) {
        //String serverHostname = new String("127.0.0.1");
        String serverHostname = new String("192.168.0.21");
        int portNum = 9991;

        System.out.println("Attemping to connect to host "
                + serverHostname + " on port "+portNum+".");

        Socket socket = null;
        PrintWriter out = null;
        BufferedReader in = null;

        try {

            socket = new Socket(serverHostname, portNum);
            out = new PrintWriter(socket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(
                    socket.getInputStream()));
        } catch (UnknownHostException e) {
            System.err.println("Unknown host " + serverHostname);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't connect to " + serverHostname);
            System.exit(1);
        }

        BufferedReader stdIn = new BufferedReader(
                new InputStreamReader(System.in));
        String userInput;

        System.out.print("Enter a message : ");
        try {
            while ((userInput = stdIn.readLine()) != null) {
                out.println(userInput);
                System.out.println("echo: " + in.readLine());
                System.out.print("Enter a message : ");
            }
        } catch (IOException ex) {
            Logger.getLogger(EchoClient.class.getName()).log(Level.SEVERE, null, ex);
        }

        try {

            out.close();
            in.close();
            stdIn.close();
            socket.close();
        } catch (IOException ex) {
            Logger.getLogger(EchoClient.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
