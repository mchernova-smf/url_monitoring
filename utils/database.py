import sqlite3
import os

root_path = "/Users/mchernova/Assigment"
DATABASE_PATH = f'{root_path}/utils/monitoring.db'
TABLE_NAME = "MONITORING"

def create_table():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(f'''CREATE TABLE {TABLE_NAME}
            (SITE               TEXT  NOT NULL,
            LAST_UPDATE         TEXT  NOT NULL,
            REQUEST_TIME        REAL  NOT NULL,
            HTTP_STATUS_CODE    INT   NOT NULL,
            HTTP_STATUS_NAME    TEXT  NOT NULL,
            CONTENT_VALIDATION  TEXT  NOT NULL);''')
    conn.close()

def insert(site, last_update, reqeust_time, http_status_code, http_status_name, content_validation):
    if not os.path.isfile(DATABASE_PATH):
        create_table()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute(f"INSERT INTO {TABLE_NAME} (SITE, LAST_UPDATE, REQUEST_TIME, HTTP_STATUS_CODE, HTTP_STATUS_NAME, CONTENT_VALIDATION) \
        VALUES ('{site}', '{last_update}', {reqeust_time}, {http_status_code}, '{http_status_name}', '{content_validation}')")
    conn.commit()
    conn.close()

def select_all():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.execute(f"SELECT * from {TABLE_NAME}")
    items = []
    for row in cursor:
        item = {}
        item["site"] = row[0]
        item["last_update"] = row[1]
        item["requst_time"] = row[2]
        item["http_status_code"] = row[3]
        item["http_status_name"] = row[4]
        item["content_validation"] = row[5]
        items += [item]
    conn.close()
    return items
