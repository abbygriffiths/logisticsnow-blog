# LogisticsNow Backend Development Assignment
A simple CRUD application to store blogs with JWT authorization. Built using Flask, SQLAlchemy, PostgresQL, and flask_jwt_extended.

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
