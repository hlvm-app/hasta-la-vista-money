[![Actions Status](https://github.com/TurtleOld/hasta-la-vista-money/workflows/hasta-la-vista-money/badge.svg)](https://github.com/TurtleOld/hasta-la-vista-money/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/cbd04aad36a00366e9ca/maintainability)](https://codeclimate.com/github/TurtleOld/hasta-la-vista-money/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/cbd04aad36a00366e9ca/test_coverage)](https://codeclimate.com/github/TurtleOld/hasta-la-vista-money/test_coverage)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)   

English version is available by [link](README_ENG.md)

# _Hasta La Vista, Money!_  

---------------------------------------------------------------------

Проект домашней бухгалтерии, который позволяет вести учёт доходов, 
расходов и просматривать различные отчёты.   

Добавлять информацию о чеках можно тремя способами:   
1. С помощью QR-кода с чека, когда магазин работает по 54-ФЗ РФ.  
Сканируем чек в приложении "ФНС. Проверка чека", таким образом добавляем чек  
в личный кабинет и делимся с ботом JSON файлом;   
> Чтобы добавлять информацию о чеке с QR-кода через приложение "ФНС. Проверка чека",   
необходимо зарегистрироваться в этом приложении.
2. С помощью текста из QR-кода: t=20230307T082500&s=XXX.XX&fn=XXXXXXXXXXXXXXXX&i=XXXXX&fp=XXXXXXXXXX&n=1   
Сканируем QR-код любым приложением и делимся с ботом текстом, который получили после сканирования;
3. Вручную, в соответствующем разделе сайта, когда нет QR-кода на чеке.  

Информация, которая собирается с чеков:
1. Информармация о продавце:  
1.1 Наименование продавца;  
1.2 Адрес покупки (Местонахождение продавца);  
1.3 Название магазина;
2. Информация о самом чеке:  
2.1 Дата покупки;  
2.2 Тип операции (Приход, возврат прихода, расход и возврат расхода);  
2.3 Итоговая сумма чека
3. Информация о продуктах из чека:  
3.1 Наименование продукта;  
3.2 Цена продукта;  
3.3 Количество;  
3.4 Итоговая сумма продукта;
   


---
#### Пример чека, как он выглядит на сайте:  
![Example Receipt](static/img/example_receipt.jpg)

---

## Установка приложения
[Инструкция по установке и запуску приложения](INSTALLATION/INSTALLATION_RUS.md)

-----------------------------------------------------------------
