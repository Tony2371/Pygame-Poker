Проект игры в покер варианта Техасский Холдем на Python. Проект пишется с применением ООП и минимальным использованием сторонних библиотек Python.

На текущий момент реализовано:
- Классы основных игровых объектов(Игрок, Колода карт, Стол)
- Функционал всех комбинаций Техасского Холдема
- Система определния сильнейшей комбинации и победителя (в т.ч. по Кикеру)

Планируется реализовать:
- Систему ставок
- GUI с использованием PyGame
- Простые алгоритмы ИИ (Always calling, Always folding, Always Raising, Always Random)


Основные классы содержатся в файле poker_main, а именно: Card, StadardDeck, Player, StandardBoard и должны быть импортированы в файл poker_run.

Для определения наличия комбинации у игрока вызывается функция evaluate() из класса Player. Она принимает один аргумент - обьект board, который является списком, содержащим текущие карты на столе. Внутри функции происходит раскладывание карт на ранги (values) и масти (suits). Затем список, содержащий ранги карт игрока складывается со списком, содержащим ранги на столе. То же самое происходит с мастями. Полученный список записывается в списки val_list и suit_list класса Player соотвественно. В дополнение к списку val_list генерируется список count_list, который имеет ту же длину и содержит integers, которые отображают количество карт того или иного ранга в val_list. Например, для набора карт(две карты игрока+пять карт на столе: [6 of ♥, 9 of ♣, 2 of ♦, Queen of ♠, 6 of ♦, 9 of ♠, 6 of ♣] count_list будет таков: [3,2,1,1,3,2,3]. Цифры 3 и 2 в списке говорят о наличии комбинации Сет (Three of a Kind) и пары, что в совокупности даёт комбинацию Full House. Одновременная итерация val_list и count_list позволяет определить какая именно карта участвует в комбинации. Тот же принцип используется для определения комбинации Flush, где идет подсчет количества мастей в списке suit_list.