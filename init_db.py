import psycopg2

from app import ticket_status_path

conn = psycopg2.connect('dbname=selectel_test user=selectel_user password=qwerty host=localhost')
cur = conn.cursor()
statement = '''
    BEGIN;
        DO $$
        BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status') THEN
        CREATE TYPE status AS ENUM (%s, %s, %s, %s);
        END IF;
        END 
        $$;
    CREATE TABLE IF NOT EXISTS ticket (
        id SERIAL PRIMARY KEY NOT NULL,
        subject VARCHAR(255) NOT NULL,
        text TEXT NOT NULL,
        email VARCHAR(255) NOT NULL,
        status status NOT NULL,
        updated_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT current_timestamp
        );
    CREATE TABLE IF NOT EXISTS comment (
        id SERIAL PRIMARY KEY NOT NULL,
        ticket_id INTEGER REFERENCES ticket(id),
        email VARCHAR(255) NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT current_timestamp
    );
    COMMIT;
'''
cur.execute(statement, ticket_status_path.keys())
conn.commit()
cur.close()
conn.close()
