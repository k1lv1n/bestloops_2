"""
Файл с парсингом данных с BestChange
"""


def get_bestchange_data():
    """
    Возвращает данные об обменниках
    :return:
    """

    pass


if __name__ == '__main__':
    from bestchange_api import BestChange

    api = BestChange()
    exchangers = api.currencies().get()
    print()
