README v1.0 / January 2020

# Utility : RoboTester

## Brief : 
RoboTester is a Machine learning based Autonomous testing utility which uses Natural Language Processing (NLP) and Supervised Machine Learning (ML) capabilities to do faster and reliable functional automation of both Web portals and Web services. It is script less automation with self learning capability, which enables Unit test cases, Story level and Regression suite automation on the fly. 

Functional validations are performed with minimum human intervention and the more you run the more smarter it becomes using it self-learning capability. It can sit on top of our existing Selenium/Python based Functional automation framework and can be the real AI/ML brain for our Automation.

Major functionalities includes, web sites and API automation, multi-OS and cross browser support, Jenkins integration, HTML test result reporting and self-learning. 

RoboTester is a sapient proprietary tool.

##Usage : 

### Execution on user system (Windows) : 
Roboster wants user to prepare some test data before execution i.e.,
	
	1. Write Manual TestCases :
		> Open excel named as 'TestCases' in the project repo.
		> Each sheet in excel workbook is considered as one manual testcase.
		> Each sheet has three columns other than 'Driver Sheet' - 'Scenario' , 'Steps' , 'Actions'.
		> Write manual testcases in natural language under 'Actions' Column.
		> While writing testcase under Actions column, It is important to put the entity under single quotes
		  i.e., User open the URl 'WWW.google.com'.
	2. Get Ready with Regression Suite :
		> Open an excel workbook named 'TestCases', it has first sheet named as 'Driver'.
		> 'Driver' sheet has Five columns - Scenario, EndToEndExecutionFlag[Y/N], RegressionExecutionFlag[Y/N],Browser and Operating System
		> 'Scenario' column represents the number of testcases with thier names.
		> 'EndToEndExecutionFlag[Y/N]' column is a flag to execute the specific number of scenarios as End to End workflow.
		> 'RegressionExecutionFlag[Y/N]' column is a flag to execute the each scenario as an independent workflow over the browser.
		> 'Browser' column is to set the type of browser i.e., Chrome,IE and Firefox
		> 'Operating System' column is to set the type of OS i.e., Windows, MAC and Linuxs
	3. Choose Proper Browser Type :
		> Open 'DriverConfig' folder in project repository.
		> Then, Open 'BrowserType' file and mention the Flag as 'Y/N' in the front of browser key.

Finally, run the 'execute' bat(in the project repository) file to initiate the Robotester.

### Execution on Jenkins : 

    1. Follow the above three steps to create test data.
	2. Push the changes into https://del.tools.publicis.sapient.com/bitbucket/projects/DAM/repos/robotester/
	3. Now create a pipeline Job using 'JenkinsFile' present in the project repository. (One time effort)
	4. Finally, Build the job to execute RoboTester.


##Installation : 

###Requirements : 
Install java version 8
Install the latest version of Python as per the OS
Install the required python libraries - using 'Imports' batch file present inside RoboTester code repository
Install Spyder (Via Anaconda) to debug python code

###SetUp : 
Clone project from github repository : https://del.tools.publicis.sapient.com/bitbucket/projects/DAM/repos/robotester/
Make sure to have all the above requirements

##Credits and Contacts : 
Varun Sharma (varun.sharma@publicissapient.com)
Ashok Yadav  (ashok.yadav@publicissapient.com)
Suraj Prakash (suraj.prakash@publicissapient.com)

#License : 
This project is licensed under Publicis Sapient. It should not be shared with the third party without informing
an oragnization. Also, any kind of modification must be conveyed before launching the after versions.




