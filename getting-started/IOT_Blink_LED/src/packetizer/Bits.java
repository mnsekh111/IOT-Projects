/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package packetizer;

/**
 *
 * @author root
 */
import java.util.BitSet;

public class Bits {

  public static BitSet convert(long value) {
    BitSet bits = new BitSet();
    int index = 0;
    while (value != 0L) {
      if (value % 2L != 0) {
        bits.set(index);
      }
      ++index;
      value = value >>> 1;
    }
    return bits;
  }

  public static long convertreverse(BitSet bits) {
    long value = 0;
    for (int i = 0; i < bits.length(); ++i) {
      value += bits.get(i) ? (1L << i) : 0L;
    }
    return value;
  }
}