BEGIN TRANSACTION;
DROP TABLE IF EXISTS skat_users CASCADE;
DROP TABLE IF EXISTS skat_years CASCADE;
DROP TABLE IF EXISTS skat_users_years CASCADE;
DROP TRIGGER IF EXISTS trigger_skat_year_changed ON skat_years CASCADE;
DROP FUNCTION IF EXISTS skat_year_changed CASCADE; 

CREATE TABLE skat_years (
    id SERIAL PRIMARY KEY NOT NULL,
    label TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    end_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
INSERT INTO skat_years VALUES(1,'2020','2020-11-24 17:20:42','2020-11-24 17:22:43','2020-01-01','2020-12-31');
INSERT INTO skat_years VALUES(2,'2021','2020-11-24 17:23:28','2020-11-24 17:23:57','2021-01-01','2021-12-31');
CREATE TABLE skat_users (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT false NOT NULL
);
INSERT INTO skat_users VALUES(7,'12345678','2020-11-24 17:24:44',1::boolean);
INSERT INTO skat_users VALUES(8,'12341234','2020-11-24 17:25:08',1::boolean);
CREATE TABLE skat_users_years (
    id SERIAL PRIMARY KEY NOT NULL,
    skat_user_id INTEGER REFERENCES skat_users(id) NOT NULL,
    skat_year_id INTEGER REFERENCES skat_years(id) NOT NULL,
    user_id VARCHAR(200) NOT NULL,
    is_paid BOOLEAN DEFAULT false NOT NULL,
    amount INT DEFAULT 0 NOT NULL
);
INSERT INTO skat_users_years VALUES(1,7,1,'12345678',1::boolean,1500);
INSERT INTO skat_users_years VALUES(2,8,1,'12341234',0::boolean,0);
CREATE FUNCTION skat_year_changed() RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF NEW.modified_at <= OLD.modified_at THEN
    NEW.modified_at := CURRENT_TIMESTAMP;
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER trigger_skat_year_changed
  BEFORE UPDATE ON skat_years
  FOR EACH ROW
  EXECUTE PROCEDURE skat_year_changed();
COMMIT;