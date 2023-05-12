from addressbook import AddressBook
from file_sorter import file_sorter
from views import *


def input_error(func):
    def execute(*args):
        try:
            return func(*args)
        except IndexError as index_error:
            return "\nThis function requires an argument.\n"
        except ValueError as value_error:
            return f"\n{value_error}\n"
        except KeyError as key_error:
            return f"\n{key_error.args[0]}\n"
        except AttributeError as attribute_error:
            return "\nAttribute doesn't exist.\n"
        except NotImplementedError:
            return "\nThis feature is not implemented\n"
    return execute


def welcome_message(*args) -> str:
    message = "\nHi! How can i help you?\n"
    return message


def help_message(*args) -> str:
    message = """
Commands and their usage:
add: 
    record 'name'                        : adds a new record with specified name.
    phone 'name' 'phone'                 : add new phone to record.
    email 'name' 'email'                 : add email to record. Can be only one.
    birthday 'name' 'birthday'           : add birthday to record. Can be only one. Birthday format dd-mm-yyyy.
    note                                 : add note to notebook.
    tags                                 : add tag(s) to the note you'll choose from notebook.
change: 
    phone 'name' 'old phone' 'new phone' : change old phone with new one.
    email 'name' 'email'                 : change email in record. 
    birthday 'name' 'birthday'           : change birthday in record. Birthday format dd-mm-yyyy.
    note                                 : change the note text.
    note title                           : change the note title.
    tags                                 : change the tags for chosen note. 
del: 
    record 'name'                        : delete record with specified name.
    phone 'name' 'phone'                 : delete phone from record.
    email 'name' 'email'                 : delete email from record.
    birthday 'name' 'birthday'           : delete birthday from record.
    note                                 : delete the note from notebook completely.
    tags                                 : delete all tags from the note.
birthdays 'number of days':              : shows contacts who have birthday in specified number of days
#:                                       : search by a tags (usage: # #tag1 #tag2...).
    """
    return message


# @input_error
def add_handler(addressbook: AddressBook, *args) -> str:
    if args[0] == 'record':
        addressbook.add_record(args[1])
        message = f'\nNew record with name {args[1]} added to addressbook.\n'
    elif args[0] == 'phone':
        addressbook[args[1]].add_phone(args[2])
        message = f'\nPhone {args[2]} added to {args[1]} record.\n'
    elif args[0] == 'email':
        addressbook[args[1]].set_email(args[2])
        message = f'\nEmail {args[2]} added to {args[1]} record.\n'
    elif args[0] == 'birthday':
        addressbook[args[1]].set_birthday(args[2])
        message = f'\nBirthday {args[2]} added to {args[1]} record.\n'
    elif args[0] == 'note':
        message = addressbook.notebook.create_note()
    elif args[0] == 'tags':
        message = addressbook.notebook.set_tags()
    else:
        message = f'\nadd does not support {args[0]} command.\n'
    return message


@input_error
def change_handler(addressbook: AddressBook, *args) -> str:
    if args[0] == 'phone':
        addressbook[args[1]].change_phone(args[2], args[3])
        message = f'\nPhone in record {args[1]} was changed from {args[2]} to {args[3]} record.\n'
    elif args[0] == 'email':
        addressbook[args[1]].set_email(args[2])
        message = f'\nEmail in record {args[1]} was changed\n'
    elif args[0] == 'birthday':
        addressbook[args[1]].set_birthday(args[2])
        message = f'\nEmail in record {args[1]} was changed\n'
    elif args[0] == 'note' and len(args) == 1:
        message = addressbook.notebook.change_note()
    elif args[0] == 'note' and args[1] == 'title':
        message = addressbook.notebook.change_title()
    elif args[0] == 'tags':
        message = addressbook.notebook.change_tags()
    else:
        message = f'\nchange does not support {" ".join(args)} command.\n'
    return message


@input_error
def del_handler(addressbook: AddressBook, *args) -> str:
    if args[0] == 'record':
        addressbook.del_record(args[1])
        message = f'\nRecord with name {args[1]} was deleted from addressbook.\n'
    elif args[0] == 'phone':
        addressbook[args[1]].del_phone(args[2])
        message = f'\nPhone {args[2]} was deleted from {args[1]} record.\n'
    elif args[0] == 'email':
        addressbook[args[1]].del_email()
        message = f'\nEmail was deleted from {args[1]} record.\n'
    elif args[0] == 'birthday':
        addressbook[args[1]].del_birthday()
        message = f'\nBirthday was deleted from {args[1]} record.\n'
    elif args[0] == 'note':
        message = addressbook.notebook.del_note()
    elif args[0] == 'tags':
        message = addressbook.notebook.del_tags()
    else:
        message = f'\ndel does not support {args[0]} command.\n'
    return message


# @input_error
def show_handler(addressbook: AddressBook, *args) -> str:
    if len(args) < 1:
        print(ConsoleContactsView.show(addressbook.data))
        return '\nAll records are shown.\n'
    elif len(args) == 1 and args[0] == 'notes':
        # mes = addressbook.notebook.show_notes()
        mes = ConsoleNotebookView.show(addressbook.notebook)
        if not mes:
            return "\nThere's no notes yet.\n"
        return mes

    return "\nSomething went wrong.\n"


@input_error
def search_handler(addressbook: AddressBook, *args):
    query = " ".join(args)
    results = addressbook.search(query)
    if not results:
        return "\nNothing was found.\n"
    return results


def find_tag(addressbook: AddressBook, *args):
    result = addressbook.notebook.find_tag(args)
    if not result:
        return "\nNo such tag(s)\n"
    print(f"\n{len(result)} note(s) was found with {' '.join(tag for tag in args)}\n")
    response = "".join(str(note) for note in result)
    return response


def save_data(addressbook: AddressBook, *args) -> str:
    addressbook.save_records_to_file('storage1.dat')
    return "\nRecords have been saved.\n"


def load_data(addressbook: AddressBook, *args) -> str:
    addressbook.read_records_from_file('storage1.dat')
    return "\nRecords have been loaded.\n"


@input_error
def sort_files(addressbook: AddressBook, *args) -> str:
    message = file_sorter(args[0])
    return message


@input_error
def list_contacts_with_days_to_birthday(addressbook: AddressBook, *args):
    birthdays = addressbook.contacts_with_days_to_bday(args[0])
    if len(birthdays) == 0:
        return f"\nNo contacts will have birthday in {args[0]} days"
    return f'\nThe following contacts will have days in {args[0]} days: \n{birthdays}'


function = {'hello': welcome_message,
            'help': help_message,
            'add': add_handler,
            'change': change_handler,
            'del': del_handler,
            'show': show_handler,
            'search': search_handler,
            'save': save_data,
            'load': load_data,
            'sort_files': sort_files,
            'birthdays': list_contacts_with_days_to_birthday,
            '#': find_tag}
