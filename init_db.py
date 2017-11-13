import psycopg2

conn = psycopg2.connect('dbname=selectel_test user=selectel_user password=qwerty')
cur = conn.cursor()
statement = '''
    BEGIN;
    CREATE TABLE IF NOT EXISTS ticket (
        id SERIAL PRIMARY KEY NOT NULL,
        subject VARCHAR(255) NOT NULL,
        text TEXT NOT NULL,
        email VARCHAR(255) NOT NULL,
        status VARCHAR(255) NOT NULL,
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
cur.execute(statement)
conn.commit()
cur.close()
conn.close()
