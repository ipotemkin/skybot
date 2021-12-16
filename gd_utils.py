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


first_row = [
    "date",
    "priority",
    "channel",
    "product",
    "group_id",
    "lesson_id",
    "reporter",
    "content",
    "source"
]


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


# TODO: not used yet
class FeedbackItem:
    def __init__(
            self,
            date=None,
            priority=None,
            channel=None,
            product=None,
            group_id=None,
            lesson_id=None,
            reporter=None,
            content=None,
            source=None
    ):
        self.date: str = date
        self.priority: int = priority
        self.channel: str = channel
        self.product: str = product
        self.group_id: str = group_id
        self.lesson_id: str = lesson_id
        self.reporter: str = reporter
        self.content: str = content
        self.source: str = source

    def __repr__(self):
        return f"<FeedbackItem (date={self.date}, content={self.content})>"

    def clear(self):
        self.date = None
        self.priority = None
        self.channel = None
        self.product = None
        self.group_id = None
        self.lesson_id = None
        self.reporter = None
        self.content = None
        self.source = None

    def is_ready(self):
        if self.channel and self.channel and self.product and self.group_id \
                and self.lesson_id and self.reporter and self.content:
            return True
        return False


class FeedbackDAO:
    def __init__(self, table_url: str = None, sheet: str = None):
        self.table_url: str = table_url
        self.cast_numbers: str = "cast_numbers=group_id,lesson_id"
        self.sheet = None
        if sheet and (sheet not in self.get_sheets()):
            self.sheet = None
            print(f"List with name={sheet} does not exist, we'll work with the first list in the book")

    def _add_sheet(self, prefix: str = "?"):
        return prefix + f"sheet={self.sheet}" if self.sheet else ""

    def get_all(self):
        s = self.table_url + "?" + self.cast_numbers + self._add_sheet("&")
        response = requests.get(s)
        assert response.status_code == HTTPStatus.OK, "Получение строк: код ответа не равен 200"
        # return response.json()
        return [FeedbackModel.parse_obj(line) for line in response.json()]

    def get_one(self, row_number: int):
        s = self.table_url + f"?limit=1&offset={row_number}" + "?" + self.cast_numbers + self._add_sheet("&")
        response = requests.get(s)
        assert response.status_code == HTTPStatus.OK
        # return response.json()
        return FeedbackModel.parse_obj(response.json()[0])

    def create(self, record: FeedbackModel):
        response = requests.post(
            self.table_url + "?" + self.cast_numbers + self._add_sheet("&"),
            json={"data": [record.dict()]},
            headers={"Content-Type": "application/json"}
        )
        print(response.status_code)
        print(response.json())
        assert response.status_code == HTTPStatus.CREATED, "Добавление строки: код ответа не равен 201"
        return response

    def update(self, record: dict, column: str, value):
        response = requests.put(
            self.table_url + f"/{column}/{value}" + "?" + self.cast_numbers + self._add_sheet("&"),
            json={"data": [record]},
            headers={"Content-Type": "application/json"}
        )
        print(response.status_code)
        print(response.json())
        assert response.status_code == HTTPStatus.OK, "Обновление строки: код ответа не равен 200"
        return response

    def delete(self, column: str, value):
        response = requests.delete(
            self.table_url + f"/{column}/{value}" + self._add_sheet(),
            headers={"Content-Type": "application/json"}
        )
        print(response.status_code)
        print(response.json())
        assert response.status_code == HTTPStatus.OK, "Удаление строки: код ответа не равен 200"
        return response

    def get_sheets(self):
        s = self.table_url + "/sheets"
        response = requests.get(s)
        assert response.status_code == HTTPStatus.OK, "Получение списка листов: код ответа не равен 200"
        return response.json()["sheets"]
        # return [FeedbackModel.parse_obj(line) for line in response.json()]

    def create_sheet(self, sheet: str):
        """
        Creates a new list (requires a special plan of usage Google docs)
        """
        s = self.table_url + "/sheet"
        response = requests.post(
            s,
            json={
                "name": sheet,
                "first_row": first_row
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == HTTPStatus.CREATED, "Добавление нового листа: код ответа не равен 201"
        # print(response.status_code)
        return response.json()


if __name__ == "__main__":
    report_table = FeedbackDAO(my_table_url, sheet="sheet5")  # , sheet="Лист1")
    print("Все строки:")
    print(*report_table.get_all(), sep='\n')

    # print("\nОдна строка:")
    # print(report_table.get_one(0))

    report_table.create(FeedbackModel.parse_obj(new_record))
    print("Все строки после добавления:")
    print(*report_table.get_all(), sep='\n')

    # report_table.update(update_record, "reporter", "Anonim")
    # print("Все строки после изменения:")
    # print(*report_table.get_all(), sep='\n')
    #
    # report_table.delete("reporter", "Goldsmith")
    # print("Все строки после удаления:")
    # print(*report_table.get_all(), sep='\n')

    # print(report_table.create_sheet("Лист3"))

    # sheets = report_table.get_sheets()
    # print("Все листы книги:", sheets)


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
