######################
Hasta La Vista, Money!
######################
.. image:: https://img.shields.io/github/actions/workflow/status/TurtleOld/hasta-la-vista-money/hasta_la_vista_money.yaml?label=Hasta%20La%20Vista%2C%20Money%21
   :alt: GitHub Workflow Status

.. image:: https://github.com/TurtleOld/hasta-la-vista-money/actions/workflows/dokku.yaml/badge.svg
   :alt: Deploy to Dokku
   :target: https://github.com/TurtleOld/hasta-la-vista-money/actions/workflows/dokku.yaml

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

|

**Отказ от ответственности:**

Проект Hasta La Vista, Money находится в активной стадии разработки, поэтому предупреждаю о возможных ошибках и изменениях в дальнейшем развитии.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Hasta La Vista, Money - это инновационный проект домашней бухгалтерии, разработанный для эффективного контроля над расходами и доходами семьи. Помимо этого, приложение обеспечивает удобный ввод данных о покупках, позволяя пользователям сканировать QR-коды с чеков передавая информацию с помощью Telegram бота или вносить информацию вручную.

Добавление информации о чеках в проект может осуществляться несколькими способами:

1. QR-коды с чеков в соответствии с 54-ФЗ РФ.
    * Сканирование чека в приложении "ФНС. Проверка чека". [#]_
    * Добавление чека в личный кабинет и передача данных в формате JSON.
2. Текст из QR-кода:
    * Сканирование QR-кода приложением и передача полученного текста в проект.
    * Пример текста: t=20230307T082500&s=XXX.XX&fn=XXXXXXXXXXXXXXXX&i=XXXXX&fp=XXXXXXXXXX&n=1.
3. **Передача фотографии или скриншота QR-кода Telegram боту.**
4. Ручной ввод данных:
    * Добавление информации о покупках вручную через соответствующий раздел на сайте.
.. [#] Для добавления чеков через приложение "ФНС. Проверка чека", необходима предварительная регистрация в этом приложении.

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


-------------------------------------------------------------------------

Contributers
============

Если вы заинтересованы в поддержке проекта, пожалуйста, ознакомьтесь с `документацией по проекту <https://hasta-la-vista-money.readthedocs.io>`_. Вместе мы можем сделать Hasta La Vista, Money еще более полезным и удобным для пользователей.
