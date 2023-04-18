from classcomands import Field, Name, Phone, Record, AddressBook, Birthday
from datetime import datetime
import re


phone_book = AddressBook()

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Give me name and phone please. For more information - enter 'Help' "
        except UnboundLocalError:
            return "You enter excessive words, please try again, or enter 'Help' "
        except KeyError:
            return "This name is not in the phone book, try again"

    return inner


def help(*args):
    return """1. To start - enter: 'Hello'
2. If you want add name and number - enter: 'add Name number' for example 'add Bill +380997654321'
3. If you want change number - enter: 'change Existing_Name old_number new_nuber' for exemple 'change Bill +380997654321'
4. If you want see phone number for name - enter 'phone Existing_Name' for exemple 'phone Bill'
5. To show all phone book - enter 'show_all'
6. To stop working - enter 'exit', 'good bye', 'close' 
7. You can add a birthday for contacts. enter 'bd Name d-m-yyyy for exemple '1-1-1991 or 21-4-2000
8. Нou can find out how many days are left until the constakt's birthday, enter 'bd <name>' \n"""



def hello(*args):
    return "Hi, how can i help you?"


def exit(*args):
    return "Good bye! =*"



@input_error
def add(*args):
    list_of_param = args[0].split()
    name = Name(list_of_param[0])
    phone = Phone(list_of_param[1])
    if len(list_of_param) > 2:
        bd = Birthday(list_of_param[2])
        rec = Record(name, phone, bd)
        phone_book.add_record(rec)
        return f"I add {name} {phone} {bd} in phone_book!"
    if name.value in phone_book.keys():
        record = phone_book[name.value]
        record.add_phone(phone)
        return f"I add {phone} to {name} in phone_book!" 
    else:
        rec = Record(name, phone)
        phone_book.add_record(rec)
        return f"I add {name} {phone} in phone_book!"


@input_error
def change(*args):
    list_of_param = args[0].split()
    name = Name(list_of_param[0])
    old_phone = Phone(list_of_param[1])
    new_phone = Phone(list_of_param[2])
    rec = phone_book.get(name.value)
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f'Phone book has no contact {name}'  


@input_error
def phone(*args):
    list_of_param = args[0].split()
    name = Name(str(list_of_param[0]).title())
    if name.value not in phone_book.keys():
        raise KeyError()
    record = phone_book[name.value]
    phones = ", ".join([str(phone) for phone in record.phones])
    return phones


@input_error
def delete(*args):
    list_of_param = args[0].split()
    name = Name(list_of_param[0])
    phone = Phone(list_of_param[1])
    rec = phone_book.get(name.value)
    if rec:
        return rec.delete_phone(phone)
    return f'Phone book has no contact {name}'  


def show_all(*args):
    list_of_param = args[0].split()
    if len(list_of_param) >= 1:
        users_num = int(list_of_param[0])
        for rec in phone_book.paginator(users_num):
            return rec
        
    result = []
    for name, phones in phone_book.items():
        result.append(f"{name}: {''.join(str(phones))}")
    return "\n".join(result)
    

def birthday(*args):
    list_of_param = args[0].title().split()
    name = Name(list_of_param[0])
    rec = phone_book.get(name.value)
    if rec:
        return rec.days_to_birthday(name)
                    


def no_command(*args):
    return "Unknown command, try again, or enter 'Help' "


COMMANDS = {help: "help",
            add: "add",
            change: "change",
            phone: "phone",
            hello: "hello",
            show_all: "showall",
            delete: "delete",
            birthday: "bd"
            # show: "show"
            }

DATE_REGEX = r"\d{1,2}([./-])\d{1,2}\1\d{4}" 

@input_error
def parser(text: str):
    tokens = text.split()
    if len(tokens) > 2:
        for i, token in enumerate(tokens):
            if token.lower() in COMMANDS.values():
                name = tokens[i + 1]
                phone = tokens[i + 2]
                try:
                    match = re.search(DATE_REGEX, tokens[i + 3]) 
                    if match:
                        date_bd = match.group()
                        result_str = f"{token.lower()} {name} {phone} {date_bd}"
                    else:
                        new_phone = tokens[i + 3]
                        result_str = f"{token.lower()} {name} {phone} {new_phone}"
                except IndexError:
                    result_str = f"{token.lower()} {name} {phone}"
    else:
        result_str = text.lower()
    return result_str


@input_error
def command_handler(text: str):
    for command, k_word in COMMANDS.items():
        if text.startswith(k_word):
            return command, text.replace(k_word, "").strip()
        if text.lower() in ["exit", "close", "good bye"]:
            return exit, None
    return no_command, None


def main():
    print(help())

    while True:
        user_input = input(">>>")
        pars = parser(user_input)
        command, data = command_handler(pars)
        print(command(data))
        if command == exit:
            break


if __name__ == "__main__":
    main()
