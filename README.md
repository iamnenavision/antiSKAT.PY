# Telegram-бот для рефакторинга кода на C++ и C
Изменяет код на C++ до неузнаваемости для противодействия списыванию на локальных контестах по Олимпиадному Программированию МАИ.
Отправьте боту код, и он сделает его очень сложным для чтения.

Списывальщикам придется потратить больше времени на его понимание, исправление стилистических ошибок, и переименование переменных, чем на написание этой же программы с нуля.

Функции:
- Меняет имена всех переменных на случайные имена с настраиваемой длиной от 1 до нескольких сотен символов.
- Удаляет все комментарии, лишние проблелы и переносы строки и добавляет случайные.
- Удаляет неиспользуемые переменные, функции и процедуры из кода.
- Вставляет директивы предпроцессора (typedef, define) и константы прямо в код.
- Добавляет быстрый вывод и return 0, если их нет.
- Делает некоторые стилистические изменения.
- Делает из кода двустрочник на C++!

Все функции можно настраивать, включать и отключать
