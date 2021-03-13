--Drop table dbo.AdobeSign_Direct_Deposit

CREATE TABLE dbo.AdobeSign_Direct_Deposit(
	completed NVARCHAR(100),
	email NVARCHAR(1000),
	role NVARCHAR(100),
	first NVARCHAR(100),
	last NVARCHAR(100),
	title NVARCHAR(100),
	company NVARCHAR(100),
	[% of Net Pay $ Amount 1] NVARCHAR(100),
	[% of Net Pay $ Amount 2] NVARCHAR(100),
	[Account Number 1] NVARCHAR(100),
	[Account Number 2] NVARCHAR(100),
	[Account Type 1] NVARCHAR(100),
	[Account Type 2] NVARCHAR(100),
	[Bank 1: Deposit Option] NVARCHAR(100),
	[Bank 2: Deposit Options] NVARCHAR(100),
	[Bank Name 1] NVARCHAR(100),
	[Bank Name 2] NVARCHAR(100),
	[Routing Number 1] NVARCHAR(100),
	[Routing Number 2] NVARCHAR(100),
	SSN NVARCHAR(100),
	[Specific $ Amount $ 1] NVARCHAR(100),
	[Specific $ Amount $ 2] NVARCHAR(100),
	[Use Information On File] NVARCHAR(100),
	agreementId NVARCHAR(1000)
)

