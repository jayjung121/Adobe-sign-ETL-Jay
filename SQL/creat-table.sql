-- drop table dbo.AdobeSign_w4;


CREATE TABLE dbo.AdobeSign_W4(
	completed NVARCHAR(100), 
	email NVARCHAR(500), 
	AddlWithholding NVARCHAR(100), 
	Address NVARCHAR(500), 
	Address2 NVARCHAR(100), 
	Claiming INT, 
	Exempt NVARCHAR(100), 
	FirstName NVARCHAR(100), 
	Group3 NVARCHAR(100), 
	LastName NVARCHAR(100), 
	SSN NVARCHAR(100)
)


select * from dbo.AdobeSign_W4