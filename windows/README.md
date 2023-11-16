## Установка на windows машины
### Требования
- должен быть установлен zabbix_sender
- python3.9 и выше. На меньших версиях не проверял

### Настройка
- клонируем репозитарий
- создаем виртуальное окружение в папке windows (python -m venv windows/venv)
- активируем окружение *venv/Scripts/activate.bat*
- ставим зависимости из папки windows
- редактируем start.bat (корректируем путь к папке windows переменная SCRIPT_PATH)
- создаем .env по анаплогии env_example
- в планировщике задач создаем запуск start.bat с правами администратора

### Если ошибка "включите переключатель loadFromRemoteSources."
### Добавляем 
<configuration>
    <runtime>
       <loadFromRemoteSources enabled="true"/>
   </runtime>
</configuration>
You can find machine.config here:

32-bit

%windir%\Microsoft.NET\Framework\[version]\config\machine.config
64-bit

%windir%\Microsoft.NET\Framework64\[version]\config\machine.config
