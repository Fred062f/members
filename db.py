import sqlite3
from data_dict import random_users
import requests
import os


required_fields = [
    ("id", int),
    ("first_name", str),
    ("last_name", str),
    ("birth_date", str),
    ("gender", str),
    ("email", str),
    ("phonenumber", str),
    ("address", str),
    ("nationality", str),
    ("active", bool),
    ("github_username", str),
]


def init_db():
    con = sqlite3.connect("app.db")
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                birth_date TEXT,
                gender TEXT,
                email TEXT,
                phonenumber TEXT,
                address TEXT,
                nationality TEXT,
                active BOOLEAN,
                github_username TEXT
                )"""
    )

    # Insert random users into table
    """users_data = [tuple(user.values()) for user in random_users]

    cur.executemany(
        "INSERT INTO members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", users_data
    )"""

    con.commit()
    con.close()


# GET
def fetch_members():
    con = sqlite3.connect("app.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM members")
    result = cur.fetchall()
    for i, member in enumerate(result):
        repositories = fetch_repositories(member)
        tup_list = list(member)
        tup_list.append(repositories)
        result[i] = tuple(tup_list)
    con.close()
    return result


# POST
def insert_member(member_data):
    validate_member_data(member_data, POST=True)

    con = sqlite3.connect("app.db")
    cur = con.cursor()

    cur.execute(
        "INSERT INTO members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        tuple(member_data.values()),
    )
    con.commit()
    con.close()


# GET
def fetch_member_by_id(id):
    if not member_exists(id):
        return False

    con = sqlite3.connect("app.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM members WHERE id = ?", (id,))
    result = cur.fetchone()

    result = list(result)
    repositories = fetch_repositories(result)
    result.append(repositories)
    con.close()
    return result


# DELETE
def delete_member_by_id(id):
    if not member_exists(id):
        return False

    con = sqlite3.connect("app.db")
    cur = con.cursor()

    cur.execute("DELETE FROM members WHERE id = ?", (id,))
    con.commit()
    con.close()
    return True


# PATCH & PUT
def update_member_by_id(id, member_data):
    if not member_exists(id):
        return False

    con = sqlite3.connect("app.db")
    cur = con.cursor()

    validate_member_data(member_data)

    fields_to_update = [f"{key} = ?" for key in member_data.keys()]
    values = list(member_data.values())

    values.append(id)

    query = f"UPDATE members SET {', '.join(fields_to_update)} WHERE id = ?"
    cur.execute(query, values)

    con.commit()
    con.close()
    return True


def fetch_repositories(result):
    github_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    github_username = result[-1]
    url = f"https://api.github.com/users/{github_username}/repos"
    headers = {"Authorization": f"token {github_access_token}"}
    req = requests.get(url, headers=headers)
    repositories = []
    if not req.status_code == 404:
        for repo in req.json():
            repositories.append(repo["name"])
    return repositories


def validate_member_data(member_data, POST=False):
    global required_fields

    if POST:
        for index, (field, field_type) in enumerate(required_fields):
            if field not in member_data:
                raise ValueError(f"Missing field: {field} in position {index}")

            if list(member_data.keys())[index] != field:
                raise ValueError(
                    f"Field '{field}' is not in the correct order (expected at position {index})"
                )

            if not isinstance(member_data[field], field_type):
                raise TypeError(
                    f"Incorrect type for field '{field}': Expected {field_type}"
                )
    else:
        required_fields = dict(required_fields)

        for field, value in member_data.items():
            if field not in required_fields:
                raise TypeError(f"{field} is not a valid field")
            if not isinstance(value, required_fields[field]):
                raise ValueError(
                    f"Incorrect type for field '{field}': Expected {required_fields[field]}, got {type(value)}"
                )


def member_exists(id):
    con = sqlite3.connect("app.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM members WHERE id = ?", (id,))
    member = cur.fetchone()

    con.close()
    return member is not None
