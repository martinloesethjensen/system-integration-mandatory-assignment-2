DROP SCHEMA IF EXISTS skat CASCADE;
CREATE SCHEMA skat;

GRANT USAGE ON SCHEMA skat TO skat_user;

CREATE TABLE skat.SkatUser (
    Id BIGSERIAL PRIMARY KEY,
    UserId VARCHAR(200) NOT NULL,
    CreatedAt VARCHAR(200) NOT NULL,
    IsActive BOOLEAN DEFAULT false
);

CREATE TABLE skat.SkatYear (
    Id BIGSERIAL PRIMARY KEY,
    Label TEXT NOT NULL,
    CreatedAt VARCHAR(200) NOT NULL,
    ModifiedAt VARCHAR(200), 
    StartDate DATE,
    EndDate DATE
);

CREATE TABLE skat.SkatUserYear (
    Id BIGSERIAL PRIMARY KEY,
    SkatUserId BIGSERIAL REFERENCES skat.SkatUser(id),
    SkatYearId BIGSERIAL REFERENCES skat.SkatYear(id),
    UserId VARCHAR(200) NOT NULL,
    IsPaid BOOLEAN DEFAULT false,
    Amount INT
);