PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS skat_users_years;
DROP TABLE IF EXISTS skat_users;
DROP TABLE IF EXISTS skat_years;
DROP TRIGGER IF EXISTS update_year_timestamps;
DROP TRIGGER IF EXISTS create_active_year;
DROP TRIGGER IF EXISTS update_active_year;
DROP TRIGGER IF EXISTS create_year;
CREATE TABLE skat_years (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    label TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    start_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    end_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT FALSE NOT NULL
);
INSERT INTO skat_years VALUES(1,'2020','2020-11-24 17:20:42','2020-11-24 17:22:43','2020-01-01T00:00:00','2020-12-31T23:59:59',1);
INSERT INTO skat_years VALUES(2,'2021','2020-11-24 17:23:28','2020-11-24 17:23:57','2021-01-01T00:00:00','2021-12-31T23:59:59',0);
CREATE TABLE skat_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id VARCHAR(200) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);
INSERT INTO skat_users VALUES(7,'2','2020-11-24 17:24:44',1);
INSERT INTO skat_users VALUES(8,'1','2020-11-24 17:25:08',1);
CREATE TABLE skat_users_years (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    skat_user_id INTEGER REFERENCES skat_users(id) NOT NULL,
    skat_year_id INTEGER REFERENCES skat_years(id) NOT NULL,
    user_id VARCHAR(200) NOT NULL,
    is_paid BOOLEAN DEFAULT false NOT NULL,
    amount REAL DEFAULT 0 NOT NULL
);
INSERT INTO skat_users_years VALUES(1,7,1,'2',1,1500);
INSERT INTO skat_users_years VALUES(2,8,1,'1',0,0);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('skat_users',8);
INSERT INTO sqlite_sequence VALUES('skat_years',2);
INSERT INTO sqlite_sequence VALUES('skat_users_years',4);
CREATE TRIGGER update_year_timestamps AFTER UPDATE ON skat_years
  FOR EACH ROW WHEN NEW.modified_at <= OLD.modified_at 
BEGIN 
  UPDATE skat_years SET modified_at=CURRENT_TIMESTAMP WHERE id=OLD.id;  
END;
CREATE TRIGGER create_active_year AFTER INSERT ON skat_years
  FOR EACH ROW WHEN NEW.is_active IS TRUE
BEGIN
  UPDATE skat_years SET is_active=FALSE WHERE id IS NOT NEW.id;
END;
CREATE TRIGGER create_year BEFORE INSERT ON skat_years
  FOR EACH ROW
BEGIN
  SELECT RAISE(ABORT, 'There can be only one year.')
    WHERE EXISTS (SELECT 1
                  FROM skat_years
                  WHERE start_date = NEW.start_date 
                  and end_date = NEW.end_date);
END;
CREATE TRIGGER update_active_year AFTER UPDATE ON skat_years
  FOR EACH ROW WHEN NEW.is_active IS TRUE
BEGIN
  UPDATE skat_years SET is_active=FALSE WHERE id IS NOT NEW.id;
END;
COMMIT;