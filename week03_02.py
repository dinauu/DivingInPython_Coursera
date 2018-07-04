import csv
from os.path import splitext


class BaseCar:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = car_type
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def get_photo_file_ext(self):
        ext = splitext(self.photo_file_name)
        return ext[1]


class Car(BaseCar):
    def __init__(self, car_type, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count


class Truck(BaseCar):
    def __init__(self, car_type, brand, photo_file_name, carrying, body_whl):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.body_whl = body_whl
        self.body_length = 0
        self.body_width = 0
        self.body_height = 0
        if self.body_whl != '':
            body_whl_split = str(self.body_whl).split('x')
            self.body_length = float(body_whl_split[0])
            self.body_width = float(body_whl_split[1])
            self.body_height = float(body_whl_split[2])

    def get_body_volume(self):
        volume = self.body_length * self.body_width * self.body_height
        return float(volume)


class SpecMachine(BaseCar):
    def __init__(self, car_type, brand, photo_file_name, carrying, extra):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_file):
    car_list = []
    with open(csv_file) as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        for car_property in reader:
            try:
                car_type = car_property[0]
                brand = car_property[1]
                photo_file_name = car_property[3]
                body_whl = car_property[4]
                carrying = car_property[5]
                if car_type == 'car':
                    passenger_seats_count = int(car_property[2])
                    car = Car(car_type=car_type, brand=brand, photo_file_name=photo_file_name, carrying=float(carrying),
                              passenger_seats_count=passenger_seats_count)
                    car_list.append(car)
                elif car_type == 'truck':
                    truck = Truck(car_type=car_type, brand=brand, photo_file_name=photo_file_name,
                                  carrying=float(carrying),
                                  body_whl=body_whl)
                    car_list.append(truck)
                elif car_type == 'spec_machine':
                    extra = car_property[6]
                    spec_machine = SpecMachine(car_type=car_type, brand=brand, photo_file_name=photo_file_name,
                                               carrying=float(carrying), extra=extra)
                    car_list.append(spec_machine)
                else:
                    print('Not found correct car type!')
            except IndexError:
                continue
    return car_list
