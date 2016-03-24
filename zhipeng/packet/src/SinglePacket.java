import java.util.BitSet;

public class SinglePacket {
	int frame_num;
	BitSet data;
	BitSet check_sum;
	static int frame_num_begin = 0;
	static int frame_num_end = 7;
	static int data_begin = 8;
	static int data_end = 20;
	static int check_begin = 21;
	static int check_end = 30;
	public SinglePacket(BitSet packet) {
		frame_num = (int) Bits.convertreverse(packet.get(frame_num_begin, frame_num_end));
		data = packet.get(data_begin, data_end);
		check_sum = packet.get(check_begin, check_end); 
		System.out.println("This is the construction function");
	}
	
	public void display() {
		System.out.println(frame_num);
		System.out.println(data);
		System.out.println(check_sum);
	}
	
}
