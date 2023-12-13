from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        phone_number VARCHAR(255),
        lang VARCHAR(20),
        location_lattitude TEXT,
        location_longetude TEXT,
        confirm TEXT
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_cats(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Category (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        description TEXT
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_subcats(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Sub_Category (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        category_id BIGINT 
        );
        """
        await self.execute(sql, execute=True)
    
    async def create_table_product(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Product (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        img_url VARCHAR(255),
        price REAL NOT NULL,
        sub_category_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)
    
    async def update_user_info_for_confirm(self, name, lang, phone_number, location_lat, location_long, confirm, telegram_id):
        sql = "UPDATE Users SET username=$1, lang=$2, phone_number=$3, location_lattitude=$4, location_longetude=$5, confirm=$6 WHERE telegram_id=$7"
        return await self.execute(sql, name, lang, phone_number, location_lat, location_long, confirm, telegram_id, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)
    
    async def user_confirm(self, telegram_id):
        sql = "SELECT confirm FROM Users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def get_all_cats(self):
        sql = "SELECT * FROM Category"
        return await self.execute(sql, fetch=True)
    
    async def get_all_sub_cats(self):
        sql = "SELECT * FROM Sub_Category"
        return await self.execute(sql, fetch=True)
    
    async def get_sub_cats_by_cat_id(self, cat_id):
        sql = "SELECT * FROM Sub_Category WHERE category_id=$1"
        return await self.execute(sql, cat_id, fetch=True)
    
    async def get_products_by_sub_cat_id(self, sub_cat_id):
        sql = "SELECT * FROM Product WHERE sub_category_id=$1"
        return await self.execute(sql, sub_cat_id, fetch=True)
    
    async def add_category(self, title, desc):
        sql = "INSERT INTO Category (title, description) VALUES($1, $2) returning *"
        return await self.execute(sql, title, desc, fetchrow=True)

    async def add_sub_category(self, title, cat_id, desc):
        sql = "INSERT INTO Sub_Category (title, description, category_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, title, desc, cat_id, fetchrow=True)
    
    async def add_product(self, title, desc, price, sub_cat_id):
        sql = "INSERT INTO Product (title, description, price, sub_category_id) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, title, desc, price, sub_cat_id, fetchrow=True)