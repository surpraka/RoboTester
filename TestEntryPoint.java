import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;
import com.relevantcodes.extentreports.ExtentReports;
import com.relevantcodes.extentreports.ExtentTest;
import com.relevantcodes.extentreports.LogStatus;

import py4j.GatewayServer;

public class TestEntryPoint {
	
	private ExtentTest test;
	private ExtentReports report;
	
	private static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss");
	
	public TestEntryPoint() {
		Timestamp timestamp = new Timestamp(System.currentTimeMillis());
		report = new ExtentReports(System.getProperty("user.dir") + "\\extent_report\\"+sdf.format(timestamp)+".html");
		test = report.startTest("ExtentDemo");
	}
	
	public void reportPass(String usermsg) {
		test.log(LogStatus.PASS, usermsg);
	}
	
	public void reportFail(String usermsg) {
		test.log(LogStatus.FAIL, usermsg);
	}

	public void reportScenario(String usermsg){
		test.log(LogStatus.PASS, usermsg);
	}
	
	public ExtentTest getTest() {
		return test ;
	}
	
	public ExtentReports getReport() {
		return report ;
	}
	
	public void endAll() {
		report.endTest(test);
		report.flush();
	}
	
	public static void main(String[] args) {
		//initialise a new gateway instance at user specified port number
		GatewayServer gatewayServer = new GatewayServer(new TestEntryPoint(),25536);
		gatewayServer.start();
		System.out.println("Gateway Server Started");
	}
}

