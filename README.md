README v1.0 / January 2020

# Utility : RoboTester

##Introduction
RoboTester is a sapient proprietary tool, which helps to automate web pages directly from manual test cases
using the concept of Machine Learing(ML) and Natural Language Processing(NLP) via Python. It has the
capability to use existing Java Frameworks, along with the support of crossbrowser testing. It extends
the support to execute testcases over jenkins also.

##Usage
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
		> 'Driver' sheet has three columns - Scenario, EndToEndExecutionFlag[Y/N], RegressionExecutionFlag[Y/N].
		> 'Scenario' column represents the number of testcases with thier names.
		> 'EndToEndExecutionFlag[Y/N]' column is a flag to execute the specific number of scenarios as End to End workflow.
		> 'RegressionExecutionFlag[Y/N]' column is a flag to execute the each scenario as an independent workflow over the browser.
	3. Choose Proper Browser Type :
		> Open 'DriverConfig' folder in project repository.
		> Then, Open 'BrowserType' file and mention the Flag as 'Y/N' in the front of browser key.

Finally, run the 'execute' bat(in the project repository) file to initiate the Robotester.

##Installation

###Requirements
Install java version 8
Install the latest version of Python as per the OS
Install the required python libraries - using 'Imports' batch file present inside RoboTester code repository
Install Spyder (Via Anaconda) to debug python code

###SetUp
Clone project from github repository : https://del.tools.publicis.sapient.com/bitbucket/projects/DAM/repos/robotester/
Make user to have all the above requirements

##Credits and Contacts
Varun Sharma (varun.sharma@publicissapient.com)
Ashok Yadav  (ashok.yadav@publicissapient.com)
Suraj Prakash (suraj.prakash@publicissapient.com)

#License
This project is licensed under Publicis Sapient. It should not be shared with the third party without informing
an oragnization. Also, any kind of modification must be conveyed before launching the after versions.




