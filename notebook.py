import re
import datetime
from collections import UserDict
from prompt_toolkit.shortcuts import prompt
from colorama import Fore, Style, init
from abc import ABC, abstractmethod
from prettytable import PrettyTable


class ConsoleView(ABC):
    @abstractmethod
    def show_info(self, data):
        raise NotImplementedError


class _HashTag:
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return f"{Fore.CYAN}#{self.tag}{Style.RESET_ALL}"

        # return f"{self.tag}"


class _Note:
    def __init__(self, note_title: str, note_text: str, tags: list[_HashTag] = None):
        self.note_title = note_title
        self.note_text = note_text
        self.tags = tags

    def __str__(self):
        init(autoreset=True)
        # tags_str = " ".join(f"{Fore.CYAN}#{tag}{Style.RESET_ALL}" for tag in self.tags)
        tags_str = " ".join(str(tag) for tag in self.tags)
        res = [
            "." * 100
            + f"\n{Fore.LIGHTWHITE_EX}{Style.BRIGHT}{self.note_title.upper().center(100)}"
            + f"{Style.RESET_ALL}\n\n{self.note_text}"
            # + f"\n{Fore.BLUE}{tags_str}{Style.RESET_ALL}\n"
            + f"\n{tags_str}\n"
            + "." * 100
            + "\n"
        ]
        return "\n".join(res)


class NoteBook(UserDict):

    def create_note(self):
        note_title = input("Enter note title: ")
        # Если заметка с таким же заголовком уже существует, то к названию плюсуеться текущее дата и время
        if note_title in self.data.keys():
            note_title += f" {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        note_content = input("Enter note text: ")
        tags_str = input("Enter tags (space separated): ").strip()
        tags_list = tags_str.split()
        tags = [_HashTag(tag.strip()) for tag in tags_list]
        new_note = _Note(note_title, note_content, tags)
        self.add_note(new_note)
        message = f"\nNote '{note_title}' created successfully!\n"
        return message

    def add_note(self, note: _Note):
        self.data[note.note_title] = note

    def _ask_note(self):
        print("\nChoose the note you want to work with.\n")
        titles = []
        for i, title in enumerate(self.data.keys(), 1):
            titles.append(title)
            print(f"{i}. {title}")
        while True:
            try:
                pos_input = input("\nEnter positional number of the note or 'exit'>>> ")
                if pos_input.lower() == "exit":
                    break
                title_pos = int(pos_input) - 1
                if title_pos > len(self.data.keys()) or title_pos < 0:
                    raise IndexError
            except IndexError:
                print("\nWrong position. Please try again.\n")
                continue
            except ValueError:
                print("\nPlease enter a valid integer index.\n")
                continue
            return titles[title_pos]

    def change_note(self):
        note_title = self._ask_note()
        if note_title is None:
            return "\nSuccessfully exited\n"
        note = self.data[note_title].note_text
        ch_note = prompt(
            f"\nChange your note (esc+ENTER to save changes):\n>>> ",
            multiline=True,
            default=note,
            validate_while_typing=True,
            enable_system_prompt=True,
            mouse_support=True
        )
        self.data[note_title].note_text = ch_note
        return f"\nNote '{note_title}' has been changed.\n"

    def del_note(self):
        note_title = self._ask_note()
        if note_title is None:
            return "\nSuccessfully exited\n"
        self.data.pop(note_title)
        return f"\nNote '{note_title}' was successfully deleted.\n"

    def show_notes(self):
        res = ""
        for note in self.data.values():
            res += f"{note}\n"
        return res

    # Поиск
    def search_note(self, query):
        results = []
        for note in self.data.values():
            if re.search(query, note.note_title, re.IGNORECASE) or re.search(
                query, note.note_text, re.IGNORECASE
            ):
                results.append(note)
        return results

    def find_tag(self, search_val: list):
        result = set()
        tag_fmt_list = [f"{Fore.CYAN}{stag}{Style.RESET_ALL}" for stag in search_val]
        for note in self.data.values():
            tag_list = [str(tag) for tag in note.tags]
            for tag in tag_list:
                if tag in tag_fmt_list:
                    result.add(note)
            # print(tag_list)
        return list(result)

    def change_title(self):
        old_title = self._ask_note()
        if old_title is None:
            return "\nSuccessfully exited\n"
        new_title = prompt("\nEdit title for the note (esc+ENTER to save changes):\n>>> ",
                           default=old_title,
                           mouse_support=True,
                           enable_system_prompt=True,
                           validate_while_typing=True)
        if old_title in self.data:
            self.data[new_title] = self.data.pop(old_title)
            self.data[new_title].note_title = new_title
        return f"\nOld title name {old_title} was change on - {new_title}\n"

    def _get_tags(self):
        if self.data.values():
            note_title = self._ask_note()
            # print(note_title)
            if note_title is None:
                return None
            tags = self.data[note_title].tags
            mes = (
                f'This note has next tags: {" ".join(str(tag) for tag in tags)}'
                if tags
                else "\nThis note hasn't any tag yet.\n"
            )
            print(mes)
            new_tags_str = input("\nEnter new tag(s):\n>>> ")
            new_tags_list = new_tags_str.split()
            new_tags = [_HashTag(tag.strip()) for tag in new_tags_list]
            return [note_title, tags, new_tags]

    def set_tags(self):
        if self.data.values():
            got_tags = self._get_tags()
            if got_tags is None:
                return "\nSuccessfully exited\n"
            tags, new_tags, title = got_tags[1], got_tags[2], got_tags[0]
            tags += new_tags
            self.data[title].tags = tags
            return "\nTags added successfully.\n"
        else:
            return "\nNo notes to set tags for.\n"

    def change_tags(self):
        if self.data.values():
            got_tags = self._get_tags()
            if got_tags is None:
                return "\nSuccessfully exited\n"
            new_tags, title = got_tags[2], got_tags[0]
            self.data[title].tags = new_tags
            return "\nTags set successfully.\n"
        else:
            return "\nNo notes to set tags for.\n"

    def del_tags(self):
        if self.data.values():
            note_title = self._ask_note()
            if note_title is None:
                return "\nSuccessfully exited\n"
            self.data[note_title].tags = []
            return "\nTags deleted successfully.\n"
        else:
            return "\nNo notes to set tags for.\n"

    def __str__(self):
        return "\n".join(str(n) for n in self.data.values())


notebook = NoteBook()


if __name__ == "__main__":
    notebook.create_note()
    notebook.create_note()
    notebook.show_notes()
    # notebook.search_note()
