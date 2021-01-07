USE [BankDb]
GO

/****** Object: Table [dbo].[Deposit] Script Date: 2020. 11. 23. 12:37:20 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Deposit] (
    [Id]         INT        IDENTITY (1, 1) NOT NULL,
    [BankUserId] INT        NOT NULL,
    [CreatedAt]  BIGINT     NOT NULL,
    [Amount]     FLOAT (53) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC),
    FOREIGN KEY ([BankUserId]) REFERENCES [dbo].[BankUser] ([UserId]) ON DELETE CASCADE ON UPDATE CASCADE
);





