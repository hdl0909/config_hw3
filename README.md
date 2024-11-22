# Описание
Этот проект представляет собой инструмент командной строки для перобразования текста из входного формата (учебный конфигурационный язык) в выходной (xml)
# Установка
Для начала, убедитесь, что у вас установлен Python. Затем выполните следующие шаги:
1.Установка программы и переход в директорию
```
git clone <URL репозитория>
cd <директория проекта>
```
2.Создайте и активируйте виртуальное окружение:
```
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
```
3.Установите необходимые зависимости (pytest для тестов)
```
pip install pytest
pip install lark
```
# Запуск скрипта
Скрипт принимает текст конфигурационного файла через стандартный ввод и выводит XML в файле.

Пример запуска:
```
python main.py text.dan output.xml
```
Здесь:
- text.dan — файл с конфигурационными данными на учебном языке.
- output.xml — файл, в который будет записан результат в формате xml.

# Примеры входных и выходных данных:
## Пример 1: Конфигурация параметров сервера
### Входные данные:
```
*> Конфигурация параметров сервера
set max_connections = 100
set timeout = 30
set server_settings = {
    max_connections = $max_connections,
    timeout = $timeout,
    ports = ( 80, 443, 8080 )
}
```
### Выходные данные (XML):
```
<constants>
  <item>
    <item>
      <comment> Конфигурация параметров сервера</comment>
    </item>
    <item>
      <set>
        <name>max_connections</name>
        <value>100</value>
      </set>
    </item>
    <item>
      <set>
        <name>timeout</name>
        <value>30</value>
      </set>
    </item>
    <item>
      <set>
        <name>server_settings</name>
        <value>
          <dict>
            <item>
              <name>max_connections</name>
              <value>100</value>
            </item>
            <item>
              <name>timeout</name>
              <value>30</value>
            </item>
            <item>
              <name>ports</name>
              <value>
                <array>
                  <item>80</item>
                  <item>443</item>
                  <item>8080</item>
                </array>
              </value>
            </item>
          </dict>
        </value>
      </set>
    </item>
  </item>
</constants>
```
## Пример 2: Конфигурация управления роботом
### Входные данные:
```
*> Параметры управления роботом
set max_speed = 10
set acceleration = 2
set movement = {
    max_speed = $max_speed,
    acceleration = $acceleration,
    waypoints = ( 0, 5, 10, 15 )
}
```
### Выходные данные (XML):
```
<constants>
  <item>
    <item>
      <comment> Параметры управления роботом</comment>
    </item>
    <item>
      <set>
        <name>max_speed</name>
        <value>10</value>
      </set>
    </item>
    <item>
      <set>
        <name>acceleration</name>
        <value>2</value>
      </set>
    </item>
    <item>
      <set>
        <name>movement</name>
        <value>
          <dict>
            <item>
              <name>max_speed</name>
              <value>10</value>
            </item>
            <item>
              <name>acceleration</name>
              <value>2</value>
            </item>
            <item>
              <name>waypoints</name>
              <value>
                <array>
                  <item>0</item>
                  <item>5</item>
                  <item>10</item>
                  <item>15</item>
                </array>
              </value>
            </item>
          </dict>
        </value>
      </set>
    </item>
  </item>
</constants>
```
# Тесты
Шаги запуска тестов:
1. Установить библиотеку pytest (необходимо, если не сделано ранее):
```
pip install pytest
```
2.Для запуска тестирования необходимо запустить следующий скрипт:
```
pytest -v
```
## Прохождение тестов:
![image](https://github.com/user-attachments/assets/f784058a-0611-4425-ad9d-d68bc227d9d2)
