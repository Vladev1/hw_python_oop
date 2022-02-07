from dataclasses import dataclass
from typing import Dict, Any, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывод данных о тренировке"""
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    SPEED_MAIN_CALORIE_COEFFICIENT: int = 18
    SPEED_MEAN_CALORIE_DEDUCTED: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Расчёт потраченных каллорий во время бега."""
        run_calories = ((self.SPEED_MAIN_CALORIE_COEFFICIENT
                        * self.get_mean_speed()
                        - self.SPEED_MEAN_CALORIE_DEDUCTED)
                        * self.weight_kg / self.M_IN_KM * self.duration_h
                        * self.MIN_IN_HR)
        return run_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LESS_IMPACT_WEIGHT_CALORIE: float = 0.035
    MAIN_INFLUENCE_WEIGHT_CALORIE: float = 0.029
    EXPONENT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        """Расчёт потраченных каллорий во время спортивной ходьбы."""
        walk_calories = ((self.LESS_IMPACT_WEIGHT_CALORIE * self.weight_kg
                          + (self.get_mean_speed()
                             ** self.EXPONENT // self.height_cm)
                          * self.MAIN_INFLUENCE_WEIGHT_CALORIE
                          * self.weight_kg)
                         * self.duration_h * self.MIN_IN_HR)
        return walk_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    ACTUAL_EFFECT_SWIM_WEIGHT: float = 2
    APPROACH_MAX_SPEED: float = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Расчёт скорости плавания."""
        swim_speed = (self.length_pool_m * self.count_pool
                      / self.M_IN_KM / self.duration_h)
        return swim_speed

    def get_spent_calories(self) -> float:
        """Расчёт потраченных каллорий во время плавания."""
        swim_calories = ((self.get_mean_speed()
                          + self.APPROACH_MAX_SPEED)
                         * self.ACTUAL_EFFECT_SWIM_WEIGHT
                         * self.weight_kg)
        return swim_calories


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    detrmining_type_training: Dict[str, Type[Any]] = {
        'RUN': Running, 'WLK': SportsWalking, 'SWM': Swimming
    }
    if workout_type not in detrmining_type_training.keys():
        raise ValueError('Трекер пока не может считать данный тип тренировки')
    return detrmining_type_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
