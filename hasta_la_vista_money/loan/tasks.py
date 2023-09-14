"""Модуль задач для пакета loan."""
import datetime

from celery import shared_task
from dateutil.relativedelta import relativedelta
from hasta_la_vista_money.constants import NumberMonthOfYear


@shared_task
def async_calculate_annuity_loan(
    id_loan,
    start_date,
    loan_amount,
    annual_interest_rate,
    period_loan,
):
    """
    Асинхронная функция по расчёту аннуитетному платежу.

    :param id_loan:
    :param start_date:
    :param loan_amount:
    :param annual_interest_rate:
    :param period_loan:
    :return:
    """
    monthly_interest_rate = float(
        (
            annual_interest_rate
            / NumberMonthOfYear.NUMBER_TWELFTH_MONTH_YEAR.value
        )
        / 100,
    )

    monthly_payment = (
        float(loan_amount)
        * (
            monthly_interest_rate
            * (1 + monthly_interest_rate) ** float(period_loan)
        )
        / ((1 + monthly_interest_rate) ** float(period_loan) - 1)
    )

    balance = loan_amount
    payment_schedule = []

    start_date = start_date + relativedelta(months=1)

    for _ in range(1, int(period_loan) + 1):
        interest = balance * monthly_interest_rate
        principal_payment = monthly_payment - interest
        balance -= principal_payment

        year = start_date.year
        month = start_date.month
        day = start_date.day
        current_date = datetime.date(year, month, day)

        next_date = start_date + relativedelta(months=1)

        payment_schedule.append(
            {
                'id': id_loan,
                'month': current_date,
                'balance': round(balance, 2),
                'monthly_payment': round(monthly_payment, 2),
                'interest': round(interest, 2),
                'principal_payment': round(principal_payment, 2),
            },
        )

        start_date = next_date

    return payment_schedule
