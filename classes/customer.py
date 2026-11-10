from classes.order import Order


class Customer:
    """Клиент: имя + список заказов."""

    def __init__(self, name: str, orders=None):
        self.name = name
        self._orders: list[Order] = []
        if orders:
            for item in orders:
                self.add_order(item)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        if not value.strip():
            raise ValueError("Имя не может быть пустым")
        self._name = value.strip()

    def add_order(self, order: Order) -> None:
        if not isinstance(order, Order):
            raise TypeError("Можно добавлять только Order")
        self._orders.append(order)

    @property
    def orders(self):
        return list(self._orders)

    @property
    def total_spent(self) -> float:
        return round(sum(o.total_price for o in self._orders), 2)

    def __len__(self):
        return len(self._orders)

    def __iter__(self):
        return iter(self._orders)

    def __getitem__(self, i):
        return self._orders[i]

    def __str__(self):
        return (
            f"Клиент: {self.name} | "
            f"заказов: {len(self)} | "
            f"потрачено: {self.total_spent:.2f} руб."
        )

    def __repr__(self):
        return f"Customer(name={self.name!r}, orders={self._orders!r})"