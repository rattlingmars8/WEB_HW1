from abc import ABC, abstractmethod
from prettytable import PrettyTable
from colorama import Fore, Style, init


class View(ABC):
    @staticmethod
    @abstractmethod
    def show(data):
        pass


class ConsoleNotebookView(View):
    @staticmethod
    def show(data):
        table = PrettyTable()
        table.field_names = ["Note Title", "Note Text", "Tags"]
        for note in data.values():
            tags_str = " ".join(str(tag) for tag in note.tags)
            table.add_row([note.note_title, note.note_text, tags_str])
        return str(table)
  

class ConsoleContactsView(View):
    @staticmethod
    def show(data):
        table = PrettyTable()
        table.field_names = ["Name", "Phones", "BDay", "Email"]
        for record in data.values():
            name = record.name.value
            str_phones = ', '.join(phone.value for phone in record.phones) if record.phones else "No records"
            str_birthday = record.birthday if record.birthday else "No records"
            str_email = record.email if record.email else "No records"
            table.add_row([name, str_phones, str_birthday, str_email])
        return str(table)



