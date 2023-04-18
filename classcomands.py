from collections import  UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __str__(self) -> str:
        return str(self.value)


class Phone(Field):
    
    def __init__(self, phone):
        self.__phone = None
        self.phone = phone
        
    
    def __str__(self) -> str:
        return str(self.phone)
    
    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        if len(value) != 13:
            raise ValueError("Phone number must have '+' and 12 digits")
        self.__phone = value
    
class Birthday:
    
    def __init__(self, value):
        self.__value = None
        self.value = value
    
    def __str__(self):
        return self.value.strftime("%d-%m-%Y")

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        try:
            datetime.strptime(value, "%d-%m-%Y")
            self.__value = datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Please enter date in format DD-MM-YYYY.")

class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday:Birthday = None):
        self.name = name
        self.phones = [phone] if phone else [] 
        self.birthday = birthday
        
    def add_phone(self, phone: Phone):
        self.phones.append(phone)
    
    # def add_birthday(self, birthday):
    #     self.birthday.append(birthday)
        
    def change_phone(self, old_phone:Phone, new_phone:Phone):
        for i, p in enumerate(self.phones):
            if p.phone == old_phone.phone:
                self.phones[i] = new_phone
                return f'Phone {old_phone} change to {new_phone}'
        return f'Contact has no phone {old_phone}'
         
    def delete_phone(self, phone:Phone):
        for i, p in enumerate(self.phones):
            if p.phone == phone.phone:
                self.phones.pop(i)
                return f'Phone {phone} deleted'

    def days_to_birthday(self, name:Name):
        if self.birthday:
            day_now = datetime.today()
            next_birthday_year = day_now.year
            if (day_now.month, day_now.day) > (self.birthday.value.month, self.birthday.value.day):
                next_birthday_year += 1
            next_birthday = datetime(next_birthday_year, self.birthday.value.month, 
                                    self.birthday.value.day)
            d_t_birthday = (next_birthday - day_now).days
            return f"{d_t_birthday} days to {self.name} birthday"
        return f"Date not found"
        
    
    def __str__(self) -> str:
        phones = ", ".join([str(phone) for phone in self.phones])
        if self.birthday:
            return f"{phones}, Birthday: {self.birthday}"
        return f"{phones}"

class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def paginator(self, users_num):
       start = 0
       while True:
           result = list(self.data)[start: start + users_num]
           result_list = [f"{key} : {self.data.get(key)}" for key in result]
           if not result:
               break
           yield "\n".join(result_list)
           start += users_num
    
    def my_search(self, query: str) -> List[Record]:
        result = []
        for name, record in self.data.items():
            if query.lower() in name.lower():
                result.append(record)
            else:
                for phone in record.phones:
                    if query in phone.phone:
                        result.append(record)
                        break
        return result
    
    def save_contacts(self, file_name):
        with open(file_name, "wb") as f:
                pickle.dump(self.data, f)
        
    def load_contacts(self, file_name):
        try:
            with open(file_name, "rb") as f:
                phone_book = pickle.load(f)
                self.data.clear()
                self.data.update(phone_book)
            
        except (FileNotFoundError, pickle.UnpicklingError):
            phone_book = None
        return phone_book   
    
