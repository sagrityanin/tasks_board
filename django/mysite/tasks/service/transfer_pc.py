import psycopg2
import os
import uuid

with open("pc.csv", "r") as s_file:
    with psycopg2.connect(host=os.getenv("POSTGRES_HOST"), user=os.getenv("POSTGRES_USER"),
                          password=os.getenv("POSTGRES_PASSWORD"),
                          database=os.getenv("POSTGRES_DB")) as pg_conn:
        cursor = pg_conn.cursor()
        for line in s_file:
            line_list = line.strip().split(",")
            query = f"insert into pc (title, telefon_number, ip, rdb_user, time_created, time_updated, id) values\
                ('{line_list[0]}', '{line_list[1]}', '{line_list[2]}', '{line_list[3]}', now(), now(), \
                     '{str(uuid.uuid4())}')"
            cursor.execute(query)
            pg_conn.commit()
        print("it is work")
