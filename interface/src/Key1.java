import java.awt.event.*;
import javax.swing.*;
class Key1 extends JFrame implements KeyListener{

    private final JTextField KeyCodeT = new JTextField("Key Code:");

    private Key1(){
        KeyCodeT.addKeyListener(this);
        KeyCodeT.setEditable(false);
        add(KeyCodeT);
        setSize(300,300);
        setVisible(true);
    }

    public void keyPressed(KeyEvent e){
        System.out.println("Key Pressed!!!");

        if(e.getKeyCode()==82) {
            JOptionPane.showMessageDialog(null,"Good  Bye");
        }
    }

    public void keyReleased(KeyEvent e){
        System.out.println("Key Released!!!");
        KeyCodeT.setText("Key Code:" + e.getKeyCode());
    }

    public void keyTyped(KeyEvent e){}

    public static void main(String[] args){
        new Key1();
    }
}

