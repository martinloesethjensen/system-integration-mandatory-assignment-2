USE [BankDb]
GO

/****** Object: Table [dbo].[Account] Script Date: 2020. 11. 23. 10:30:30 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Account] (
    [Id]         INT        IDENTITY (1, 1) NOT NULL,
    [BankUserId] INT        NOT NULL,
    [AccountNo]  INT        NOT NULL,
    [IsStudent]  BIT        NOT NULL,
    [CreatedAt]  BIGINT     NOT NULL,
    [ModifiedAt] BIGINT     NOT NULL,
    [Amount]     FLOAT (53) NOT NULL
);


