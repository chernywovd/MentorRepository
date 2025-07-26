import random
from Database.Database import DatabaseClass
from apscheduler.schedulers.asyncio import AsyncIOScheduler


rand_mentor = DatabaseClass(TgUserID=6027246732)

async def mix_the_mentors():
    "Функция по перемешиванию менторов (всех, кроме блатных, они остаются сверху)"
    call_order = await rand_mentor.select_rows(SelectQuery=f"SELECT CallOrder FROM mentors ORDER BY Id;")
    call_order_list = [item['CallOrder'] for item in call_order]
    # print(call_order_list)

    # Находим индексы всех единиц
    indices_of_ones = [i for i, x in enumerate(call_order_list) if x == 1]

    # Удаляем все единицы из списка
    lst_without_ones = [x for x in call_order_list if x != 1]

    # Перемешиваем оставшиеся элементы
    new_call_order_list = random.sample(lst_without_ones, len(lst_without_ones))

    # Проходимся по списку индексов и в new_call_order_list возвращаем единицы
    for index in indices_of_ones:
        new_call_order_list.insert(index, 1)

    # print(new_call_order_list)

    list_str_val = ['(' + str(v) + ')' for v in new_call_order_list ]
    # print(list_str_val)

    # Объединяем значения в одну строку с для корректного sql запроса
    result = ", ".join(list_str_val)
    # print(result)

    #Создаём временную таблицу
    await rand_mentor.create_table(Query=f"CREATE TABLE tempupdates "
                                           f"(TempId INT PRIMARY KEY AUTO_INCREMENT, NewValue INT);")

    await rand_mentor.insert_query(InsertQuery=f"INSERT INTO tempupdates (NewValue) "
                                                 f"VALUES {result};")


    await rand_mentor.update_query(UpdateQuery=f"UPDATE mentors JOIN tempupdates "
                                                 f"ON mentors.Id = tempupdates.TempId "
                                                 f"SET mentors.CallOrder = tempupdates.NewValue;")

    #Удаляем временную таблицу
    await rand_mentor.drop_table(Query=f"DROP TABLE tempupdates;")


# Функция для запуска планировщика
async def scheduler_mix():
    scheduler = AsyncIOScheduler()

    # Планируем выполнение функции mix_the_mentors ночью в 3 часа 20 минут
    scheduler.add_job(mix_the_mentors, 'cron', hour=3, minute=20)

    # Запускаем планировщик
    scheduler.start()
