/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package packetizer;

import packetizer.Bits;
import java.util.BitSet;

/**
 *
 * @author root
 */
public class SinglePacket2 {

    public int frame_num;
    public BitSet data;
    public BitSet check_sum;
    public static int frame_num_begin = 0;
    public static int frame_num_end = 7;
    public static int data_begin = 8;
    public static int data_end = 20;
    public static int check_begin = 21;
    public static int check_end = 30;

    /**
     * Use this function to customize the packet properties 
    */
    public static void initSinglePacket(int fbegin, int fend, int dbegin, int dend, int cbegin, int cend) {
        frame_num_begin = fbegin;
        frame_num_end = fend;
        data_begin = dbegin;
        data_end = dend;
        check_begin = cbegin;
        check_end = cend;
    }

    public SinglePacket2(BitSet packet) {
        frame_num = (int) Bits.convertreverse(packet.get(frame_num_begin, frame_num_end));
        data = packet.get(data_begin, data_end);
        check_sum = packet.get(check_begin, check_end);
        //System.out.println("This is the construction function");
    }

    public void display() {
        System.out.println(frame_num);
        System.out.println(data);
        System.out.println(check_sum);
    }
}
