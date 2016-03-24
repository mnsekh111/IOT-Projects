import java.io.DataInputStream;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStream;

public final class BitInputStream extends DataInputStream {

    public static final int MAX_BITS = 31;

    private int leftBits = 0;
    private int byteBuf = 0;

    public BitInputStream(InputStream in) {
        super(in);
    }

    public final boolean readBit() throws IOException {
        if(--leftBits >= 0) {
            return ((byteBuf >>> leftBits) & 1) == 1;
        }
        leftBits = 7;
        byteBuf = in.read();
        if(byteBuf == -1) {
            throw new EOFException("reached end of stream");
        }
        return ((byteBuf >>> 7) & 1) == 1;
    }

    public final int readBits(int n) throws IOException {
        int x = 0;
        while(n > leftBits) {
            n -= leftBits;
            x |= rightBits(leftBits, byteBuf) << n;
            byteBuf = in.read();
            if(byteBuf == -1) {
                throw new EOFException("reached end of stream");
            }
            leftBits = 8;
        }
        leftBits -= n;
        return x | rightBits(n, byteBuf >>> leftBits);
    }

    private static final int rightBits(int n, int x) {
        return x & ((1 << n) - 1);
    }
}
