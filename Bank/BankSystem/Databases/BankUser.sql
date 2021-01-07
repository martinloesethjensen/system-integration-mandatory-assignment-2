USE [BankDb]
GO

/****** Object: Table [dbo].[BankUser] Script Date: 2020. 11. 21. 23:17:47 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[BankUser] (
    [Id]         INT    IDENTITY (1, 1) NOT NULL,
    [UserId]     INT    NOT NULL UNIQUE,
    [CreatedAt]  BIGINT NOT NULL,
    [ModifiedAt] BIGINT NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC),
    UNIQUE NONCLUSTERED ([UserId] ASC)
);



