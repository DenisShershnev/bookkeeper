"""
Описан класс, представляющий бюджет
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Budget:
    """
    Бюджет.
    category - id категории расходов
    summa - сумма
    term - срок
    pk - id записи в базе данных
    """
    category: int
    summa: float
    term: datetime = field(default_factory=datetime.now)
    pk: int = 0
