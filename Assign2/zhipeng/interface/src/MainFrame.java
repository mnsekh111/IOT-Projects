import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import javax.swing.JFrame;

class MainFrame extends JFrame implements KeyListener{
    /**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private final MainDraw draw;

    public void keyPressed(KeyEvent e) {
        System.out.println("keyPressed");
    }

    public void keyReleased(KeyEvent e) {
        if(e.getKeyCode()== KeyEvent.VK_RIGHT)
            draw.moveRight();
        else if(e.getKeyCode()== KeyEvent.VK_LEFT)
            draw.moveLeft();
        else if(e.getKeyCode()== KeyEvent.VK_DOWN)
            draw.moveDown();
        else if(e.getKeyCode()== KeyEvent.VK_UP)
            draw.moveUp();
        System.out.println(e.getKeyChar());

    }
    public void keyTyped(KeyEvent e) {
        System.out.println("keyTyped");
    }

    private MainFrame(){
        this.draw=new MainDraw();
        addKeyListener(this);
        setFocusable(true);
        setFocusTraversalKeysEnabled(false);
    }

    public static void main(String[] args) {
        javax.swing.SwingUtilities.invokeLater(() -> {
            MainFrame frame = new MainFrame();
            frame.setTitle("Square Move Practice");
            frame.setResizable(false);
            frame.setSize(600, 600);
            frame.setMinimumSize(new Dimension(600, 600));
            frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            frame.getContentPane().add(frame.draw);
            frame.pack();
            frame.setVisible(true);
        });
    }
}