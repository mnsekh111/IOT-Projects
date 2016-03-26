package iot;
import java.nio.ByteBuffer;
import java.util.zip.*;

public class CheckSum {

	// The checksum is 2 bytes
	public static byte[] checkSum16(byte[] bytes) {
	    int crc = 0xFFFF;

	    for (int j = 0; j < bytes.length ; j++) {
	        crc = ((crc  >>> 8) | (crc  << 8) )& 0xffff;
	        crc ^= (bytes[j] & 0xff);  //byte to int, trunc sign
	        crc ^= ((crc & 0xff) >> 4);
	        crc ^= (crc << 12) & 0xffff;
	        crc ^= ((crc & 0xFF) << 5) & 0xffff;
	    }
	   
	    byte[] result = new byte[2];
	    result[0] = (byte)(crc);   // Here has the byte order problem. The byte 0 stores the higher part of lower part checksum;
	    result[1] = (byte)(crc >> 8);
	    return result;
	}
	
	// The checksum is 4 bytes;
	public static byte[] checkSum(byte[] data) {
		CRC32 checkSumCal = new CRC32();
		checkSumCal.update(data, 0, data.length);
		
		ByteBuffer buffer = ByteBuffer.allocate(Long.BYTES);
		buffer.putLong(checkSumCal.getValue());
		return buffer.array();
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("1234");
		String data = "1234";
		byte[] dataByte = data.getBytes();
		checkSum(dataByte);
		
	}

}
