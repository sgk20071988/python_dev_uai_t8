from classes.customer import Customer
from classes.discount import Discount
from classes.order import Order
from classes.product import Product


def main():
    # -------- 1. Продукты --------
    print("=" * 65)
    print("ПРОДУКТЫ")
    print("=" * 65)
    laptop     = Product("Ноутбук", 75000)
    mouse      = Product("Мышь", 1500.5)
    keyboard   = Product("Клавиатура", 3200)
    monitor    = Product("Монитор", 18000)
    headphones = Product("Наушники", 4500)
    webcam     = Product("Веб-камера", 2700)
    usb_hub    = Product("USB-хаб", 900)
    chair      = Product("Кресло", 12000)
    products = [laptop, mouse, keyboard, monitor, headphones, webcam, usb_hub, chair]

    for p in products:
        print(f"  str:  {p}")
    print()

    order1 = Order([laptop, mouse])
    order2 = Order([headphones])
    order3 = Order([monitor, keyboard])
    order4 = Order([mouse, keyboard])
    order5 = Order([webcam, usb_hub])
    order6 = Order([chair, webcam, usb_hub])
    orders = [order1, order2, order3, order4, order5, order6]

    Discount.apply_to_order(order1, [Discount("Скидка новичкам", 10)])
    Discount.apply_to_order(order2, [Discount("Сезонная распродажа", 20)])
    Discount.apply_to_order(order3, [
        Discount("Чёрная пятница", 15),
        Discount("Промокод BOB5", 5),
    ])
    Discount.apply_to_order(order4, [Discount("Промокод SAVE20", 20)])
    Discount.apply_to_order(order6, [Discount("Распродажа мебели", 12)])

    print()
    print("=" * 65)
    print("ЗАКАЗЫ С ПРИМЕНЕННЫМИ СКИДКАМИ")
    print("=" * 65)
    for i, order in enumerate(orders, start=1):
            print(f"{i}. {order}")

    print()
    print("=" * 65)
    print("КЛИЕНТЫ")
    print("=" * 65)
    alice, bob, charlie = Customer("Алиса"), Customer("Боб"), Customer("Чарли")
    customers = [alice, bob, charlie]

    alice.add_order(order1)
    alice.add_order(order2)

    bob.add_order(order3)
    bob.add_order(order6)

    charlie.add_order(order4)
    charlie.add_order(order5)
    
    for c in customers:
        print(f"  {c}")
    print()

    total_orders = sum(len(c) for c in customers)
    total_sum = round(sum(c.total_spent for c in customers), 2)

    print(f"Всего заказов: {total_orders}")
    print(f"Общая сумма: {total_sum:.2f} руб.")


if __name__ == "__main__":
    main()