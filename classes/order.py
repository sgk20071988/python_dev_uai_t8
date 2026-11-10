from collections.abc import Iterable

from classes.product import Product


class Order:
    """Класс, представляющий заказ с набором товаров."""

    def __init__(self, products: Iterable["Product"] | None = None):
        # Приватный список — доступ через свойство products
        self._products: list[Product] = []
        if products:
            for p in products:
                self.add_product(p)

    @property
    def products(self) -> list["Product"]:
        """Возвращает копию списка, чтобы нельзя было изменить его извне."""
        return list(self._products)

    def add_product(self, product: "Product") -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product")
        self._products.append(product)

    def remove_product(self, product: "Product") -> None:
        try:
            self._products.remove(product)
        except ValueError:
            raise ValueError(f"Товар {product!r} отсутствует в заказе")

    def clear(self) -> None:
        self._products.clear()

    def replace_products(self, new_products) -> None:
        """Заменить товары заказа (используется при применении скидок)."""
        new_products = list(new_products)
        if len(new_products) != len(self._products):
            raise ValueError("Количество товаров не должно меняться")
        for p in new_products:
            if not isinstance(p, Product):
                raise TypeError("Ожидается Product")
        self._products = new_products

    @property
    def total_price(self) -> float:
        """Суммарная стоимость заказа."""
        return sum(p.price for p in self._products)

    def __len__(self) -> int:
        return len(self._products)

    def __iter__(self):
        return iter(self._products)

    def __getitem__(self, index: int) -> "Product":
        return self._products[index]

    def __str__(self) -> str:
        if not self._products:
            return "Заказ пуст"
        lines = ["Заказ:"]
        lines += [f"  - {p}" for p in self._products]
        lines.append(f"Итого: {self.total_price:.2f} руб. (позиций: {len(self)})")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Order(products={self._products!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self._products == other._products

    def __lt__(self, other) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.total_price < other.total_price