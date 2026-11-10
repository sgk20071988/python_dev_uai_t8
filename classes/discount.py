from classes.order import Order
from classes.product import Product


class Discount:
    """Скидка: описание + процент (0..100)."""

    def __init__(self, description: str, discount_percent: float):
        self.description = description
        self.discount_percent = discount_percent

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Описание должно быть строкой")
        if not value.strip():
            raise ValueError("Описание не может быть пустым")
        self._description = value.strip()

    @property
    def discount_percent(self) -> float:
        return self._discount_percent

    @discount_percent.setter
    def discount_percent(self, value: float):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Процент должен быть числом")
        if not 0 <= value <= 100:
            raise ValueError("Процент должен быть в диапазоне от 0 до 100")
        self._discount_percent = float(value)

    @staticmethod
    def _validate_amount(amount):
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
        return float(amount)
    
    @staticmethod
    def stacked(amount, discounts):
        result = Discount._validate_amount(amount)
        for d in discounts:
            if isinstance(d, Discount):
                result = d.apply(result)                      # объект Discount
            elif isinstance(d, (int, float)) and not isinstance(d, bool):
                result = Discount.percent(result, d)          # просто число = процент
            else:
                raise TypeError("Ожидается Discount или число-процент")
        return round(result, 2)

    @staticmethod
    def apply_to_order(order: "Order", discounts=None) -> float:
        """Применить скидки к заказу, изменив цены товаров внутри него.

        Оригинальные Product-объекты НЕ мутируются: в заказ кладутся копии
        с новыми ценами, поэтому другие заказы с теми же товарами не страдают.
        Возвращает новую сумму заказа.
        """
        if not isinstance(order, Order):
            raise TypeError("Ожидается Order")

        discounts = discounts or []
        if not discounts:
            return order.total_price

        old_total = order.total_price
        if old_total == 0:
            return 0.0

        new_total = Discount.stacked(old_total, discounts)
        ratio = new_total / old_total

        # Пропорционально пересчитываем цену каждого товара
        new_products = [
            Product(p.name, round(p.price * ratio, 2)) for p in order.products
        ]

        # Убираем расхождение округления: подгоняем последний товар,
        # чтобы сумма в точности совпала с new_total
        delta = round(new_total - sum(p.price for p in new_products), 2)
        if delta and new_products:
            last = new_products[-1]
            new_products[-1] = Product(last.name, round(last.price + delta, 2))

        order.replace_products(new_products)
        return order.total_price
    
    @property
    def multiplier(self) -> float:
        """Во сколько раз уменьшается сумма (1 - percent/100)."""
        return 1 - self.discount_percent / 100

    def apply(self, amount: float) -> float:
        """Применяет скидку к сумме и возвращает итоговую сумму."""
        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной")
        return round(amount * self.multiplier, 2)

    def __call__(self, amount: float) -> float:
        """Позволяет использовать скидку как функцию: d(1000)."""
        return self.apply(amount)

    def __str__(self) -> str:
        return f"{self.description} (-{self.discount_percent:g}%)"

    def __repr__(self) -> str:
        return (
            f"Discount(description={self.description!r}, "
            f"discount_percent={self.discount_percent!r})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Discount):
            return NotImplemented
        return (self.description, self.discount_percent) == (
            other.description, other.discount_percent
        )

    def __lt__(self, other) -> bool:
        """Сортировка скидок по проценту."""
        if not isinstance(other, Discount):
            return NotImplemented
        return self.discount_percent < other.discount_percent