USE [BankDb]
GO

/****** Object: Table [dbo].[Loan] Script Date: 2020. 11. 23. 12:48:57 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Loan] (
    [Id]         INT        IDENTITY (1, 1) NOT NULL,
    [BankUserId] INT        NOT NULL,
    [CreatedAt]  BIGINT     NOT NULL,
    [ModifiedAt] BIGINT     NOT NULL,
    [Amount]     FLOAT (53) NOT NULL
);



