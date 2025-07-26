import random
from Database.Database import DatabaseClass
from Sub.Subjects import dict_directions

from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Глобальная переменная для хранения актуальных данных
current_mentors_data = None



mentors_from_db = DatabaseClass(TgUserID=6027246732)


async def select_mentors_from_db():
    subject_list = list(dict_directions.values())
    subject_dict = {subject: [] for subject in subject_list} # составляем словарь с напрвлениянми

    # Добавляем в возвращаемый словарь информацию о ментроах из базы
    all_mentors_info = await mentors_from_db.select_rows(SelectQuery=f"SELECT * FROM mentors WHERE "
                                                              f"Activity = 1 ORDER BY CallOrder;")

    dict_info_from_db = {}
    dict_info_from_db["Информация о менторах из базы"] = all_mentors_info

    # Добавляем в возвращаемый словарь отсортированных наставников по направлениям
    for info in all_mentors_info:
        subj = info["Subject"]
        try:
            subject_dict[subj].append(info)
        except Exception as ex:
            pass

    dict_info_from_db["Отсортированные наставники по направлениям"] = subject_dict


    list_user_mentor = await mentors_from_db.select_rows(SelectQuery=f"SELECT u.* FROM mentors m JOIN users u "
                                                      f"ON m.IdTgUserId = u.Id WHERE u.Activity = 1;")


    list_user_mentor = list({frozenset(d.items()): d for d in list_user_mentor}.values()) # удалям дубликаты словарей

    dict_info_from_db["Наставники из таблицы users"] = list_user_mentor

    return dict_info_from_db # возвращаем словарь с Информацией о менторах из базы и Отсортированных наставниках по направлениям

async def update_mentors_data():
    global current_mentors_data
    current_mentors_data = await select_mentors_from_db()

async def scheduler_update_data_mentors():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_mentors_data, 'interval', seconds=90)  # Обновляем раз в час
    scheduler.start()
    await update_mentors_data()  # Первоначальная загрузка данных
