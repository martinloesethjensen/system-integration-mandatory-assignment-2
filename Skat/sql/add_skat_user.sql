INSERT INTO skat.SkatUser(UserId, CreatedAt, IsActive)
VALUES ($1, $2, $3)
RETURNING $table_fields;