USE SUPPLYPLANNING_NEW;
GO

CREATE TABLE Depart_ModifiedRevenue_Log (
    IDLog INT IDENTITY(1,1) PRIMARY KEY, 
    IDRevenue INT NOT NULL,  
    Year INT NOT NULL, 
    Month TINYINT NOT NULL, 
    Units INT NOT NULL,  
    Revenue DECIMAL NOT NULL,  
    Fob_per_unit DECIMAL NOT NULL,  
    Comment VARCHAR(255),  
    Goal DECIMAL(18, 2), 
    StatusRevenue INT DEFAULT 1,  
    CreateDate DATETIME NULL,
    LastUpdate DATETIME NULL,  
    ActionType VARCHAR(10) NOT NULL,  
    LogDate DATETIME DEFAULT GETDATE() 


    CONSTRAINT FK_Depart_ModifiedRevenue FOREIGN KEY (IDRevenue)
    REFERENCES Depart_ModifiedRevenue(IDRevenue)
);


/*
SELECT * FROM Depart_ModifiedRevenue_Log
*/