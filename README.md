# Что
В общем и целом, файл туда, файл сюда и в продакшн

# Как
Единственный важный момент файл `config.ini` должен лежать рядом с исполняемым файлом, потом что иначе мне было лень изворачиваться.   

В самом `config.ini` надо задать три параметра. На всякий случай продублирую здесь, хотя пример конфига есть в репозитории

* `DRC_SOURCE` : путь до входного файла. Лучше задавать его полным, чтоб точно.
* `DEST` : сюда будет созранен Excel файлик. Для надежности лучне тоже задать полный путь.
* `NUM_CH` : число каналов, которое я так и не спарсил из файла. Если задать не правильно, то поперепутает к чертям данные на стыке буферов. Не надо в нем ошибаться.

Как только все задали, запускаем приложение. Должна открыться консоль. Если она открывается и сразу пропадает, значит что-то пошло не по плану с системными либами. Если увидели надпись `Just read logs and press ENTER`. То радуемся все сработало.