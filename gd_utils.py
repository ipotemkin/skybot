import requests
from http import HTTPStatus
from pydantic import BaseModel
from typing import Optional

# my_table_url = "https://docs.google.com/spreadsheets/d/1IlBohmQ9aY8HfarZppPzoOapLct9mm7WFEFvmsODGl8/edit?usp=sharing"
my_table_url = "https://sheetdb.io/api/v1/fvrwdnv55a5pt"

new_record = {
    "date": '14.12.2021',
    "priority": '2',
    "channel": 'prof-pd-1_0-hw-api-flask-14',
    "product": 'pd',
    "group_id": '1',
    "lesson_id": '14',
    "reporter": 'Anonim',
    "content": 'В тренажере на 9 странице не работает “Привет%“',
    "source": 'https://app.slack.com/client/T0290F60PQ8/C02BGKYHJDU/user_profile/U02BX5LA1M3'
}

update_record = {
    "reporter": 'Goldsmith',
}


class FeedbackModel(BaseModel):
    date: str
    priority: int
    channel: str
    product: str
    group_id: int
    lesson_id: int
    reporter: str
    content: str
    source: Optional[str]

    class Config:
        orm_mode = True


class FeedbackItem:
    def __init__(self, date, priority, channel, product, group_id, lesson_id, reporter, content, source=None):
        self.date: str = date
        self.priority: int = priority
        self.channel: str = channel
        self.product: str = product
        self.group_id: str = group_id
        self.lesson_id: str = lesson_id
        self.reporter: str = reporter
        self.content: str = content
        self.source: str = source


class FeedbackDAO:
    def __init__(self, table_url: str = None):
        self.table_url: str = table_url
        self.cast_numbers: str = "?cast_numbers=group_id,lesson_id"

    def get_all(self):
        response = requests.get(self.table_url + self.cast_numbers)
        assert response.status_code == HTTPStatus.OK, "Получение строк: код ответа не равен 200"
        # return response.json()
        return [FeedbackModel.parse_obj(line) for line in response.json()]

    def get_one(self, row_number: int):
        r_url = self.table_url + f"?limit=1&offset={row_number}"
        response = requests.get(r_url)
        assert response.status_code == HTTPStatus.OK
        # return response.json()
        return FeedbackModel.parse_obj(response.json()[0])

    def create(self, record: FeedbackModel):
        response = requests.post(
            self.table_url,
            json={"data": [record.dict()]},
            headers={"Content-Type": "application/json"}
        )
        print(response.status_code)
        print(response.json())
        assert response.status_code == HTTPStatus.CREATED, "Добавление строки: код ответа не равен 201"
        return response

    def update(self, record: dict, column: str, value):
        r_url = self.table_url + f"/{column}/{value}"
        response = requests.put(
            r_url,
            json={"data": [record]},
            headers={"Content-Type": "application/json"}
        )
        print(response.status_code)
        print(response.json())
        assert response.status_code == HTTPStatus.OK, "ОБновление строки: код ответа не равен 200"
        return response

    def delete(self, column: str, value):
        r_url = self.table_url + f"/{column}/{value}"
        response = requests.delete(
            r_url,
            headers={"Content-Type": "application/json"}
        )
        print(response.status_code)
        print(response.json())
        assert response.status_code == HTTPStatus.OK, "Удаление строки: код ответа не равен 200"
        return response


if __name__ == "__main__":
    report_table = FeedbackDAO(my_table_url)
    print("Все строки:")
    print(*report_table.get_all(), sep='\n')
    print("\nОдна строка:")
    print(report_table.get_one(0))

    report_table.create(FeedbackModel.parse_obj(new_record))
    print("Все строки после добавления:")
    print(*report_table.get_all(), sep='\n')

    report_table.update(update_record, "reporter", "Anonim")
    print("Все строки после изменения:")
    print(*report_table.get_all(), sep='\n')

    report_table.delete("reporter", "Goldsmith")
    print("Все строки после удаления:")
    print(*report_table.get_all(), sep='\n')


# date='9.12.2021',
# priority=2,
# channel='prof-pd-1_0-hw-api-flask-14',
# product='pd',
# group_id='1',
# lesson_id='14',
# reporter='Igor Potemkin',
# content='В тренажере на 9 странице не работает “Привет%“',
# source='https://app.slack.com/client/T0290F60PQ8/C02BGKYHJDU/user_profile/U02BX5LA1M3'


# print(response.status_code)
#
# content = response.json()
#
# print(*content, sep='\n')
