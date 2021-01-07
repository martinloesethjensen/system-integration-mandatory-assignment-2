CREATE DATABASE BankDb;
GO

USE [BankDb]
GO
/****** Object: Table [dbo].[BankUser] Script Date: 2020. 11. 24. 17:34:43 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[BankUser] (
    [Id]         INT    IDENTITY (1, 1) NOT NULL,
    [UserId]     INT    NOT NULL,
    [CreatedAt]  BIGINT NOT NULL,
    [ModifiedAt] BIGINT NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC),
    UNIQUE NONCLUSTERED ([UserId] ASC)
);

USE [BankDb]
GO
/****** Object: Table [dbo].[Account] Script Date: 2020. 11. 24. 17:34:06 ******/
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
    [Amount]     FLOAT (53) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC),
    UNIQUE NONCLUSTERED ([BankUserId] ASC),
    UNIQUE NONCLUSTERED ([AccountNo] ASC),
    FOREIGN KEY ([BankUserId]) REFERENCES [dbo].[BankUser] ([UserId]) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

USE [BankDb]
GO

/****** Object: Table [dbo].[Deposit] Script Date: 2020. 11. 24. 17:35:13 ******/
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

USE [BankDb]
GO

/****** Object: Table [dbo].[Loan] Script Date: 2020. 11. 24. 17:35:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Loan] (
    [Id]         INT        IDENTITY (1, 1) NOT NULL,
    [BankUserId] INT        NOT NULL,
    [CreatedAt]  BIGINT     NOT NULL,
    [ModifiedAt] BIGINT     NOT NULL,
    [Amount]     FLOAT (53) NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC),
    FOREIGN KEY ([BankUserId]) REFERENCES [dbo].[BankUser] ([UserId]) ON DELETE CASCADE ON UPDATE CASCADE
);

insert into BankUser (UserId, CreatedAt, ModifiedAt) values (1, 1111111111, 1111111111)
insert into Account (BankUserId,AccountNo,IsStudent,CreatedAt,ModifiedAt,Amount) values (1,1,0,1111111111,1111111111,100000)







