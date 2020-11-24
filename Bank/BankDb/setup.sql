CREATE DATABASE BankDb;
GO

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
    [Amount]     FLOAT (53) NOT NULL
);
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
    [ModifiedAt] BIGINT NOT NULL
);

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
    [Amount]     FLOAT (53) NOT NULL
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
    [Amount]     FLOAT (53) NOT NULL
);










