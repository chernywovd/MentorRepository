from Database.mysql import host, user, password, db_name
import asyncio
import aiomysql
import aiomysql.cursors
import datetime



class DatabaseClass:

    def __init__(self, TgUserID):
        self.TgUserID = TgUserID #айди юзера в телеграмме

    async def check_user_in_the_list(self):
        '''Метод для проверки нахождения пользователя в бд (для команды /start)'''
        try:
            connection = await aiomysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db=db_name,
                cursorclass=aiomysql.DictCursor
                )
            user_in_the_list = False  # Инициализация переменной
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute(f"SELECT id FROM users WHERE TgUserID = '{self.TgUserID}';")
                    rows_users = await cursor.fetchall()

                    # Проверка на то, зарегистрировался пользователь или нет
                    if len(rows_users) == 0:
                        user_in_the_list = False
                    else:
                        user_in_the_list = True
                    await connection.commit()

            finally:
                connection.close()

        except Exception as ex:
            print('Не работает метод check_user_in_the_list')
            print(ex)

        return user_in_the_list


    async def insert_user(self):
        '''Метод для внесения пользователя в бд'''
        try:
            connection = await aiomysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db=db_name,
                cursorclass=aiomysql.DictCursor
                )
            try:
                async with connection.cursor() as cursor:
                    """Если пользователя нет в бд, то заносим его"""
                    check_user = DatabaseClass(TgUserID=self.TgUserID)
                    if await check_user.check_user_in_the_list() == False:  # пользователя нет в бд
                        insert_query = f"INSERT INTO users(TgUserId, DateOfRegistration) " \
                                       f"VALUES ({self.TgUserID}, NOW() );"  # заносим
                        await cursor.execute(insert_query)
                    else:
                        pass
                    await connection.commit()

            finally:
                connection.close()

        except Exception as ex:
            print('Не работает метод insert_user')
            print(ex)



    async def select_user(self):
        '''Метод, который позволяет достать данные пользователя'''
        try:
            connection = await aiomysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db=db_name,
                cursorclass=aiomysql.DictCursor
                )
            try:
                async with connection.cursor() as cursor:
                    select_rows_users = f"SELECT * FROM users WHERE TgUserID = '{self.TgUserID}';"
                    await cursor.execute(select_rows_users)
                    row_user = await cursor.fetchall()
                    await connection.commit()
            finally:
                connection.close()

        except Exception as ex:
            print('Не работает метод select_user')
            print(ex)
        return row_user[0]


    async def select_rows(self, SelectQuery):
        '''Метод, который вытаскивает записи из в таблицы'''
        try:
            connection = await aiomysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db=db_name,
                cursorclass=aiomysql.DictCursor
                )
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute(SelectQuery)
                    row = await cursor.fetchall()
                    await connection.commit()
            finally:
                connection.close()

        except Exception as ex:
            print('Не работает метод select_rows')
            print(ex)
        return row



    async def update_query(self, UpdateQuery):
        '''Метод, который изменяет данные в таблицах'''
        try:
            connection = await aiomysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db=db_name,
                cursorclass=aiomysql.DictCursor
                )
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute(UpdateQuery)
                    await connection.commit()
            finally:
                connection.close()

        except Exception as ex:
            print('Не работает метод update_query')
            print(ex)



    async def insert_query(self, InsertQuery):
        '''Метод для внесения данных в базу'''
        try:
            connection = await aiomysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db=db_name,
                cursorclass=aiomysql.DictCursor
                )
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute(InsertQuery)
                    await connection.commit()

            finally:
                connection.close()

        except Exception as ex:
            print('Не работает метод insert_query')
            print(ex)




    async def create_table(self, Query: str):
        '''Метод для создания столбцов'''
        try:
            connection = await aiomysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db=db_name,
                cursorclass=aiomysql.DictCursor
                )
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute(Query)
                    await connection.commit()

            finally:
                connection.close()

        except Exception as ex:
            print('Не работает метод create_table')
            print(ex)

    async def drop_table(self, Query: str):
        '''Метод для удаления столбцов и таблиц'''
        try:
            connection = await aiomysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db=db_name,
                cursorclass=aiomysql.DictCursor
                )
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute(Query)
                    await connection.commit()

            finally:
                connection.close()

        except Exception as ex:
            print('Не работает метод drop_table')
            print(ex)


    async def delete_query(self, Query: str):
        '''Метод для удаления значений в базе'''
        try:
            connection = await aiomysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db=db_name,
                cursorclass=aiomysql.DictCursor
                )
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute(Query)
                    await connection.commit()

            finally:
                connection.close()

        except Exception as ex:
            print('Не работает метод delete_query')
            print(ex)