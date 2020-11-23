USE [BankDb]
GO

/****** Object: Table [dbo].[Deposit] Script Date: 2020. 11. 23. 10:38:27 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Deposit] (
    [Id]         INT        NOT NULL,
    [BankUserId] INT        NOT NULL,
    [CreatedAt]  BIGINT     NOT NULL,
    [Amount]     FLOAT (53) NOT NULL
);


