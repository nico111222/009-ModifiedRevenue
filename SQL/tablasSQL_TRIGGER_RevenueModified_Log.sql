
	
USE SUPPLYPLANNING_NEW;
GO

CREATE TRIGGER TR_Depart_ModifiedRevenue_Log_INSERT
ON Depart_ModifiedRevenue
FOR INSERT
AS
BEGIN
    -- Insertar el nuevo registro en el log con la acción "INSERT"
    INSERT INTO Depart_ModifiedRevenue_Log 
    (IDRevenue, Year, Month, Units, Revenue, Fob_per_unit, Comment, Goal, StatusRevenue, CreateDate, LastUpdate, ActionType)
    SELECT IDRevenue, Year, Month, Units, Revenue, Fob_per_unit, Comment, Goal, StatusRevenue, CreateDate, LastUpdate, 'INSERT'
    FROM INSERTED;  -- La tabla INSERTED contiene los datos del nuevo registro insertado
END;
GO

---------------------------------------
CREATE TRIGGER TR_Depart_ModifiedRevenue_Log_UPDATE
ON Depart_ModifiedRevenue
FOR UPDATE
AS
BEGIN
    -- Insertar los valores actualizados en el log con la acción "UPDATE"
    INSERT INTO Depart_ModifiedRevenue_Log 
    (IDRevenue, Year, Month, Units, Revenue, Fob_per_unit, Comment, Goal, StatusRevenue, CreateDate, LastUpdate, ActionType)
    SELECT I.IDRevenue, I.Year, I.Month, I.Units, I.Revenue, I.Fob_per_unit, I.Comment, I.Goal, I.StatusRevenue, I.CreateDate, I.LastUpdate, 'UPDATE'
    FROM INSERTED I;  -- La tabla INSERTED contiene los valores después de la actualización
END;
GO


----------------------------------------
USE SUPPLYPLANNING_NEW;
GO

CREATE TRIGGER TR_Depart_ModifiedRevenue_Log_DELETE
ON Depart_ModifiedRevenue
FOR DELETE
AS
BEGIN
    -- Actualizar el StatusRevenue a 0 en lugar de eliminar el registro
    UPDATE DMR
    SET DMR.StatusRevenue = 0
    FROM Depart_ModifiedRevenue DMR
    INNER JOIN DELETED D ON DMR.IDRevenue = D.IDRevenue;

    -- Insertar en el log la acción de "DELETE", aunque solo estamos actualizando
    INSERT INTO Depart_ModifiedRevenue_Log 
    (IDRevenue, Year, Month, Units, Revenue, Fob_per_unit, Comment, Goal, StatusRevenue, CreateDate, LastUpdate, ActionType)
    SELECT D.IDRevenue, D.Year, D.Month, D.Units, D.Revenue, D.Fob_per_unit, D.Comment, D.Goal, D.StatusRevenue, D.CreateDate, D.LastUpdate, 'DELETE'
    FROM DELETED D;  -- La tabla DELETED contiene los registros eliminados (antes del update)
END;
GO

