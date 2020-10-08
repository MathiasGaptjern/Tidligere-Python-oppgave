package Gruppe_8;
// Gjort i fellesskap av kandidatnr 125, 150 og 129.
import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JButton;

public class Hovedvindu extends JFrame implements ActionListener {
	private JPanel contentPane;
	private Lærer lærer = new Lærer();
	private Student student = new Student();
	private Kontroll kontroll = Kontroll.getInstance();

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Hovedvindu frame = new Hovedvindu();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	public Hovedvindu() {
		setTitle("Hovedvindu");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		try {
			kontroll.lagForbindelse();
		} catch (Exception e) {
			e.printStackTrace();
		}
		setBounds(100, 100, 313, 173);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);

		JButton btnLærer = new JButton("Lærer");
		btnLærer.addActionListener(this);
		btnLærer.setBounds(54, 51, 78, 21);
		contentPane.add(btnLærer);

		JButton btnStudent = new JButton("Student");
		btnStudent.addActionListener(this);
		btnStudent.setBounds(169, 51, 91, 21);
		contentPane.add(btnStudent);

		JButton btnAvslutt = new JButton("Avslutt");
		btnAvslutt.addActionListener(this);
		btnAvslutt.setBounds(204, 105, 85, 21);
		contentPane.add(btnAvslutt);
	}

	public void actionPerformed(ActionEvent e) {
		String valg = e.getActionCommand();
		if (valg.equals("Lærer")) {
			lærer.LærerVindu();
		} else if (valg.equals("Student")) {
			student.LoggInnVindu();
		} else if (valg.equals("Avslutt")) {
			System.exit(0);
		}
	}

}
