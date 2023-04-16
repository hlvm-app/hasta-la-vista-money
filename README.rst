.. image:: https://img.shields.io/github/actions/workflow/status/TurtleOld/hasta-la-vista-money/hasta_la_vista_money.yaml?label=Hasta%20La%20Vista%2C%20Money%21
   :alt: GitHub Workflow Status

.. image:: https://api.codeclimate.com/v1/badges/cbd04aad36a00366e9ca/maintainability
   :target: https://codeclimate.com/github/TurtleOld/hasta-la-vista-money/maintainability
   :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/cbd04aad36a00366e9ca/test_coverage
   :target: https://codeclimate.com/github/TurtleOld/hasta-la-vista-money/test_coverage
   :alt: Test Coverage

.. image:: https://img.shields.io/badge/style-wemake-000000.svg
   :target: https://github.com/wemake-services/wemake-python-styleguide

.. image:: https://www.codefactor.io/repository/github/turtleold/hasta-la-vista-money/badge
   :target: https://www.codefactor.io/repository/github/turtleold/hasta-la-vista-money
   :alt: CodeFactor


======================
Hasta La Vista, Money!
======================

`Документация по проекту <https://hasta-la-vista-money.readthedocs.io>`_


Hasta La Vista, Money - проект домашней бухгалтерии для контроля расходов и доходов семьи с возможностью просмотра отчётов

Проект даёт возможность не только контролировать расходы и доходы, но и упрощает внесение данных о покупках.
Для этого необходимо просканировать QR-код с чека. Когда QR-кода нет на чеке, есть возможность внесение покупок вручную.

|

Добавлять информацию о чеках можно тремя способами:

1. С помощью QR-кода с чека, когда магазин работает по 54-ФЗ РФ.
   Сканируем чек в приложении "ФНС. Проверка чека", таким образом добавляем чек
   в личный кабинет и делимся с ботом JSON файлом; [#]_
2. С помощью текста из QR-кода: t=20230307T082500&s=XXX.XX&fn=XXXXXXXXXXXXXXXX&i=XXXXX&fp=XXXXXXXXXX&n=1
   Сканируем QR-код любым приложением и делимся с ботом текстом, который получили после сканирования; [#]_
3. Вручную, в соответствующем разделе сайта, когда нет QR-кода на чеке.

.. [#] Чтобы добавлять информацию о чеке с QR-кода через приложение "ФНС. Проверка чека",
   необходимо зарегистрироваться в этом приложении.

.. [#] Для этого потребуется указать ИНН и пароль от личного кабинета налоговой.

|

Информация, которая собирается с чеков:

1. Информация о продавце:
      1. Наименование продавца;
      2. Адрес покупки (Местонахождение продавца);
      3. Название магазина;
2. Информация о самом чеке:
      1. Дата покупки;
      2. Тип операции (Приход, возврат прихода, расход и возврат расхода);
      3. Итоговая сумма чека
3. Информация о продуктах из чека:
      1. Наименование продукта;
      2. Цена продукта;
      3. Количество;
      4. Итоговая сумма продукта;
      5. Тип НДС;
      6. Сумма НДС;


|

Пример чека, как он выглядит на сайте:

.. image:: static/img/example_receipt.jpg


