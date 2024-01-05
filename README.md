# LogisticsNow Backend Development Assignment
A simple CRUD application to store blogs with JWT authorization. Built using Flask, SQLAlchemy, PostgresQL, and flask_jwt_extended.

### Set-up and Running
- To set up the environment, start a new Conda environment using `conda env -n 'env_name' create -f environment.yml` (Replace env_name with an environment name of your choice)
- Activate environment using `conda activate 'env_name'`
- Ensure Postgres server is running on port 5432
- Ensure values are present in `.env` file according to section Environment Variables.
- Run server using `python api.py`


### Environment Variables
Create a .env file in the root directory of the project. In it, ensure the following key value pairs are present.
Values used during development are *NOT* being provided for security reasons.

DB_USERNAME=`postgres_username`
DB_PASSWD=`postgres_password`
DB_NAME=`postgres_db_name`
DB_HOST=`postgres_host_url`
DB_PORT=`postgres_host_port`

JWT_SECRET_KEY=`a secret key for signing jwt`

### Database Schema
posts_development=# \dt
         List of relations
 Schema | Name | Type  |   Owner
--------+------+-------+-----------
 public | blog | table | abirbhavg
 public | user | table | abirbhavg
(2 rows)

posts_development=# \d blog
                           Table "public.blog"
  Column   |            Type             | Collation | Nullable | Default
-----------+-----------------------------+-----------+----------+---------
 id        | character varying(36)       |           | not null |
 title     | character varying(100)      |           | not null |
 content   | text                        |           | not null |
 author    | character varying(50)       |           | not null |
 timestamp | timestamp without time zone |           |          |
Indexes:
    "blog_pkey" PRIMARY KEY, btree (id)

posts_development=# \d user
                                       Table "public.user"
    Column     |         Type          | Collation | Nullable |             Default
---------------+-----------------------+-----------+----------+----------------------------------
 id            | integer               |           | not null | nextval('user_id_seq'::regclass)
 username      | character varying(50) |           | not null |
 password_hash | character varying(60) |           | not null |
Indexes:
    "user_pkey" PRIMARY KEY, btree (id)
    "user_username_key" UNIQUE CONSTRAINT, btree (username)
