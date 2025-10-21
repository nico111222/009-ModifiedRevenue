/*
Crear tabla para informacion de revenue
*/
USE SUPPLYPLANNING_NEW;
GO

CREATE TABLE Depart_ModifiedRevenue (
    IDRevenue INT IDENTITY(1,1) PRIMARY KEY,
    Year INT NOT NULL,
    Month TINYINT NOT NULL,
    Units INT NOT NULL,
    Revenue DECIMAL NOT NULL,
    Fob_per_unit DECIMAL NOT NULL,
    Comment VARCHAR(255),
    Goal DECIMAL(18, 2),
    StatusRevenue INT DEFAULT 1,
    CreateDate datetime NULL,
    LastUpdate datetime NULL

	CONSTRAINT UQ_Year_Month UNIQUE (Year, Month)
);

/*
ALTER TABLE Depart_ModifiedRevenue 
    ALTER COLUMN CreateDate SET DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE Depart_ModifiedRevenue 
    ALTER COLUMN LastUpdate SET DEFAULT CURRENT_TIMESTAMP;

*/


/*
SELECT * FROM Depart_ModifiedRevenue
*/

INSERT INTO Depart_ModifiedRevenue (Year, Month, Units, Revenue, Fob_per_unit, Comment, Goal, StatusRevenue)
VALUES
(2025, 1, 1500, 50000.00, 33.33, 'Este es un comentario de prueba', 52000.00, 1),
(2025, 1, 1200, 40000.00, 33.33, 'Otro comentario de prueba', 42000.00, 1);


update Depart_ModifiedRevenue set StatusRevenue=0
from Depart_ModifiedRevenue
where IDRevenue=1
