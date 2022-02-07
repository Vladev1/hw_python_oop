class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
    training_type: str,
    duration: float,
    distance: float,
    speed: float,
    calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вывод данных о тренировке"""
        return (f"Тип тренировки: {self.training_type}; "
        f"Длительность: {self.duration:.3f} ч.; "
        f"Дистанция: {self.distance:.3f} км; "
        f"Ср. скорость: {self.speed:.3f} км/ч; "
        f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HR: int = 60

    def __init__(self,
    action: int,
    duration: float,
    weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def __init__(self, 
    action: int,
    duration: float,
    weight: float,
    ) -> None:
        super().__init__(action,duration, weight)

    def get_spent_calories(self) -> float:
        """Расчёт потраченных каллорий во время бега."""
        run_calories = ((self.coeff_calorie_1 * self.get_mean_speed() 
        - self.coeff_calorie_2)
        * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_HR)
        return run_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: float = 0.029
    EXPONENT: float = 2

    def __init__(self,
    action: int,
    duration: float,
    weight: float,
    height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        
    def get_spent_calories(self) -> float:
        """Расчёт потраченных каллорий во время спортивной ходьбы."""
        walk_calories = ((self.coeff_calorie_3 * self.weight + 
        (self.get_mean_speed() ** self.EXPONENT // self. height) * 
        self.coeff_calorie_4 * self.weight) * self.duration * self.MIN_IN_HR)
        return walk_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coef_weight: float = 2
    coef_speed: float = 1.1

    def __init__(self,
    action: int,
    duration: float,
    weight: float,
    count_pool: float,
    length_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        
    def get_mean_speed(self) -> float:
        """Расчёт скорости плавания."""
        swim_speed = (self.length_pool * self.count_pool /
        self.M_IN_KM / self.duration)
        return swim_speed

    def get_spent_calories(self) -> float:
        """Расчёт потраченных каллорий во время плавания."""
        swim_calories = ((self.get_mean_speed() + 
        self.coef_speed) * self.coef_weight * self.weight)
        return swim_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary: dict = {'RUN': Running, 'WLK': SportsWalking, 'SWM': Swimming}
    return dictionary[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)