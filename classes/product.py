class Product:
    """Класс, представляющий товар."""

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Название должно быть строкой")
        if not value.strip():
            raise ValueError("Название не может быть пустым")
        self._name = value.strip()

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Цена должна быть числом")
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = float(value)

    def __str__(self) -> str:
        return f"{self.name} — {self.price:.2f} руб."

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.price!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.price == other.price

    def __lt__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price