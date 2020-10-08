package Gruppe_8;

import java.io.BufferedReader;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.StringTokenizer;


public class Kontroll {
	private String databasenavn = "jdbc:mysql://localhost:3306/kurs?serverTimezone=UTC";
	private String databasedriver = "com.mysql.jdbc.Driver";
	private Connection forbindelse;
	private ResultSet resultat;
	private Statement utsagn;
	private int nokkel;
	private int nokkelSpm;
	private ArrayList<Svar> svar = new ArrayList();
	private String LAGREFIL1 = "Svar.txt";

	// Oppretter forbindelse med databasen
	public void lagForbindelse() throws Exception {
		try {
			forbindelse = DriverManager.getConnection(databasenavn, "Kurs", "Surk");
		} catch (Exception e) {
			throw new Exception("Kan ikke oppnå kontakt med databasen" + e);
		}
	}
	
	// Finner student for logg inn funksjon ved hjelp av studentens navn og passord
	public ResultSet finnStudent(String studNavn, String studPassord) throws Exception {
		resultat = null;
		try {
			String sqlSetning = "select * from tblstudent where studNavn = '" + studNavn + "' and studPassord = '"
					+ studPassord + "';";
			utsagn = forbindelse.createStatement();
			resultat = utsagn.executeQuery(sqlSetning);
		} catch (Exception e) {
			throw new Exception(e);
		}
		return resultat;
	}

	// Finner hva studenten svarte på spørsmål og alternativ for kvitteringen ved hjelp av studentID og evalueringsID 
	public ResultSet finnSvar(int studID, int evalID) throws Exception {
		resultat = null;
		try {
			String sqlSetning = "select svarStudID, altTekst, spmTekst from tblSvar, tblalternativ, tblsporsmal\r\n"
					+ "where svarStudID = " + studID + " AND spmEvalID = " + evalID
					+ " AND svarAltID = altID AND altSpmID = spmID;";
			utsagn = forbindelse.createStatement();
			resultat = utsagn.executeQuery(sqlSetning);
		} catch (Exception e) {
			throw new Exception(e);
		}
		return resultat;
	}
	
	// Finner hvilke evalueringer studenten har mulighet for å besvare basert på deres ID
	public ResultSet finnUndersøkelse(int ID) throws Exception {
		resultat = null;
		try {
			String sqlSetning = "select distinct skStudID, evalID, evalNavn, kursnavn, evalDatoInn, evalDatoUt\r\n"
					+ "from tblKurs, tblstudkurs, tblevaluering, tblSvar, tblalternativ, tblsporsmal\r\n"
					+ "where skStudID = '" + ID + "' \r\n" + "	and skKursID = evalKursID \r\n"
					+ "	and evalKursID = kursID\r\n"
					+ "    and evalID NOT IN (SELECT evalID FROM tblKurs, tblevaluering, tblSvar, tblalternativ, tblsporsmal WHERE svarStudID = skStudID\r\n"
					+ "		and svarAltID = altID\r\n" + "		and altSpmID = spmID\r\n"
					+ "		and spmEvalID = evalID\r\n"
					+ "		and evalKursID = kursID) and evalDatoUt < now() and evalDatoInn > now();";
			utsagn = forbindelse.createStatement();
			resultat = utsagn.executeQuery(sqlSetning);
		} catch (Exception e) {
			throw new Exception(e);
		}
		return resultat;
	}

	// Finner spørsmål basert på evalueringsID
	public ResultSet finnSpørmål(int evalID) throws Exception {
		resultat = null;
		try {
			String sqlSetning = "SELECT spmTekst, spmID FROM tblsporsmal where  spmEvalID = " + evalID + ";";
			utsagn = forbindelse.createStatement();
			resultat = utsagn.executeQuery(sqlSetning);
		} catch (Exception e) {
			throw new Exception(e);
		}
		return resultat;
	}

	// Finner alternativer basert på spørsmålID
	public ResultSet finnAlternativ(int spmID) throws Exception {
		resultat = null;
		try {
			String sqlSetning = "SELECT altTekst, altID FROM tblalternativ WHERE altSpmID = " + spmID + ";";
			utsagn = forbindelse.createStatement();
			resultat = utsagn.executeQuery(sqlSetning);
		} catch (Exception e) {
			throw new Exception(e);
		}
		return resultat;
	}

	// Lagrer hvilket svar alternativ som ble valgt
	public void lagreSvar(int studID, int altID) throws Exception {
		if (altID != 0) {
			String sqlsetning = "INSERT INTO tblsvar VALUES(" + studID + "," + altID + ");";
			try {
				Statement utsagn = forbindelse.createStatement();
				utsagn.executeUpdate(sqlsetning);
			} catch (Exception ex) {
				throw new Exception("Klarte ikke å lagre");
			}
		}
	}
	
	// Metoden for å lagre data om evaluering til database. Bruker Statement.RETURN_GENERATED_KEYS for å 
	// hente ut den nyeste AUTO_INCREMENTED nøkkelen fra databasen.
	public void lagreEval(String kursID, String evaluering, String datoUt, String datoInn) throws Exception {
		Statement utsagn = null;
		ResultSet rs = null;
		lagForbindelse();
		try {
			utsagn = forbindelse.createStatement();
			utsagn.executeUpdate("INSERT INTO kurs.tblevaluering (evalID, evalKursID, evalNavn, evalDatoUt, evalDatoInn)"
								+ " VALUES (" + null + ",'" + kursID + "','" + evaluering + "','" + datoUt + "','" + datoInn + "');",
								Statement.RETURN_GENERATED_KEYS);
			nokkel = -1;
			rs = utsagn.getGeneratedKeys();
			if (rs.next()) {
				nokkel = rs.getInt(1);
			}
			
			// lukker resultat dersom den er åpen
			if (rs != null) {
				try {
					rs.close();
				} catch(Exception e) {System.out.println("Feil, får ikke lukket resultat" + e);}
			}
			
			// Lukker utsagn dersom den er åpen
			if (utsagn != null) {
				try {
					utsagn.close();
				} catch(Exception e) {System.out.println("Feil, får ikke lukket utsagn" + e);}
			}
		} catch(Exception e) {}
	}
	
	// Metoden for å lagre data om spørsmål til database. Bruker Statement.RETURN_GENERATED_KEYS for å 
	// hente ut den nyeste AUTO_INCREMENTED nøkkelen fra databasen.
	public void lagreSpm(String spm) throws Exception {
		Statement utsagn = null;
		ResultSet rs = null;
		try {
			lagForbindelse();
			utsagn = forbindelse.createStatement();
			utsagn.executeLargeUpdate("INSERT INTO kurs.tblsporsmal (spmID, spmEvalID, spmTekst)"
					+ " VALUES (" + null + "," + nokkel + ",'" + spm + "');",
					Statement.RETURN_GENERATED_KEYS);
			nokkelSpm = -1;
			rs = utsagn.getGeneratedKeys();
			if (rs.next()) {
				nokkelSpm = rs.getInt(1);
			}
			
			// Lykker resultat dersom den er åpen
			if (rs != null) {
				try {
					rs.close();
				} catch(Exception e) {System.out.println("Feil, får ikke lukket resultat" + e);}
			}
			
			// Lukker utsagn dersom den er åpen
			if (utsagn != null) {
				try {
					utsagn.close();
				} catch(Exception e) {System.out.println("Feil, får ikke lukket utsagn" + e);}
			}
		} catch(Exception e) {System.out.print(e);}
	}
	
	// Metoden for å lagre data om alternativ til database. Sjekker om alternativene inneholder data før den
	// blir sendt over til databasen.
	public boolean lagreAlt(String alt1, String alt2, String alt3, String alt4, String alt5) throws Exception {
		boolean resultat = false;
		try {
			lagForbindelse();
			if (!alt1.isEmpty()) {
				utsagn = forbindelse.createStatement();
				String sql = "INSERT INTO kurs.tblalternativ (altID, altSpmID, altTekst)"
						+ " VALUES (" + null + "," + nokkelSpm + ",'" + alt1 + "');";
				Statement utsagn = forbindelse.createStatement();
				resultat = utsagn.execute(sql);
			}
			if (!alt2.isEmpty()) {
				utsagn = forbindelse.createStatement();
				String sql = "INSERT INTO kurs.tblalternativ (altID, altSpmID, altTekst)"
						+ " VALUES (" + null + "," + nokkelSpm + ",'" + alt2 + "');";
				Statement utsagn = forbindelse.createStatement();
				resultat = utsagn.execute(sql);
			}
			if (!alt3.isEmpty()) {
				utsagn = forbindelse.createStatement();
				String sql = "INSERT INTO kurs.tblalternativ (altID, altSpmID, altTekst)"
						+ " VALUES (" + null + "," + nokkelSpm + ",'" + alt3 + "');";
				Statement utsagn = forbindelse.createStatement();
				resultat = utsagn.execute(sql);
			}
			if (!alt4.isEmpty()) {
				utsagn = forbindelse.createStatement();
				String sql = "INSERT INTO kurs.tblalternativ (altID, altSpmID, altTekst)"
						+ " VALUES (" + null + "," + nokkelSpm + ",'" + alt4 + "');";
				Statement utsagn = forbindelse.createStatement();
				resultat = utsagn.execute(sql);
			}
			if (!alt5.isEmpty()) {
				utsagn = forbindelse.createStatement();
				String sql = "INSERT INTO kurs.tblalternativ (altID, altSpmID, altTekst)"
						+ " VALUES (" + null + "," + nokkelSpm + ",'" + alt5 + "');";
				Statement utsagn = forbindelse.createStatement();
				resultat = utsagn.execute(sql);
			}
			// Lukker utsagn
			utsagn.close();
		} catch (Exception e) {System.out.println("Feil oppstått" + e);}
		return resultat;
	}
	
	// Metode for å slette svar fra evaluering
	public ResultSet slettSvar() throws Exception {
		ResultSet resultat = null;
		String søkOrd = Rapport.søkElement2();
		try {
			lagForbindelse();
			utsagn = forbindelse.createStatement();
			utsagn.executeUpdate("DELETE FROM tblsvar WHERE svarAltID = "+ søkOrd +";");
			//Lukker utsagn
			utsagn.close();
		} catch(Exception e) {System.out.println("Feil oppstått" + e);}
		return resultat;
	}
	
	//Kodet av kandidat: 129
    //Lager en metode for nySvar, som er nødvendig for lagre ny svar til fil.
	public void nySvar(String skStudID, String svarAltID) {
  		svar.add(new Svar(skStudID, svarAltID));
  	}
    
  	//For å finne riktig KursID
    public ResultSet finnSvar() throws Exception {
    	ResultSet resultat = null;
    	String søkeOrd = Rapport.søkElement1();
    	try {
    		String sqlSetning = "select svarStudID, svarAltID from tblSvar, tblAlternativ, tblSporsmal, tblEvaluering, tblKurs\r\n" + 
    							"where svarAltID = altID and altspmID = spmID and spmEvalID = evalID and evalKursID = kursID and kursID = '"+ søkeOrd +"';";
            utsagn = forbindelse.createStatement();
            resultat = utsagn.executeQuery(sqlSetning);
            
    	} catch(Exception e){
                throw new Exception("Finner ikke ordre" + e);
            } //catch                 
                return resultat;        
        } //metode

    
  	//Lagrer filer på flatfil basert på
    public void lagreSvar() {
		try {
			ResultSet alleSvar = finnSvar();
			while(alleSvar.next()) {
				String studID = alleSvar.getString(1);
				String altID = alleSvar.getString(2);
				nySvar(studID,altID);
			}
			
			PrintWriter utfil = InnUt.lagSkriveForbindelse1(LAGREFIL1);
			for(int i = 0;i < svar.size();i++) {
				Object sv = svar.get(i);
				utfil.println(sv.toString());
			}
			utfil.close();
		}catch(Exception e) {}
	}
	
    //Leser fra flatfil inn i arraylisten svar
	public void lesSvar() {
		svar.clear();
		try{
			BufferedReader innfil = InnUt.lagLeseForbindelse1(LAGREFIL1);
			String linje = innfil.readLine();
			while(linje != null) {			
				StringTokenizer innhold = new StringTokenizer(linje,",");
				String skStudID = innhold.nextToken();
				String svarAltID = innhold.nextToken();
				svar.add(new Svar(skStudID,svarAltID));		
				linje = innfil.readLine();
			}
			innfil.close();
		}catch(Exception e){}
	}

	public static Kontroll getInstance() {
		return KontrollHolder.INSTANCE;
	}

	private static class KontrollHolder {
		public static final Kontroll INSTANCE = new Kontroll();
	}
}
