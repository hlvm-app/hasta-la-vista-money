"""Модуль задач для пакета loan."""
import datetime

from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404
from hasta_la_vista_money.constants import NumberMonthOfYear
from hasta_la_vista_money.loan.models import Loan, PaymentSchedule
from hasta_la_vista_money.users.models import User


@shared_task
def async_calculate_annuity_loan(
    user_id,
    loan_id,
    start_date,
    loan_amount,
    annual_interest_rate,
    period_loan,
):
    """
    Асинхронная функция по расчёту аннуитетных платежей.

    :param user_id:
    :param loan_id:
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

    start_date = start_date + relativedelta(months=1)

    user = get_object_or_404(User, id=user_id)

    loan = get_object_or_404(
        Loan,
        id=loan_id,
    )

    for _ in range(1, int(period_loan) + 1):
        interest = balance * monthly_interest_rate
        principal_payment = monthly_payment - interest
        balance -= principal_payment

        year = start_date.year
        month = start_date.month
        day = start_date.day
        current_date = datetime.date(year, month, day)

        next_date = start_date + relativedelta(months=1)
        PaymentSchedule.objects.create(
            user=user,
            loan=loan,
            date=current_date,
            balance=round(balance, 2),
            monthly_payment=round(monthly_payment, 2),
            interest=round(interest, 2),
            principal_payment=round(principal_payment, 2),
        )

        start_date = next_date


@shared_task
def async_calculate_differentiated_loan(
    user_id,
    loan_id,
    start_date: datetime.datetime,
    loan_amount: float,
    annual_interest_rate: float,
    period_loan: int,
):
    """
    Асинхронная функция по расчёту дифференцированных платежей.

    :param user_id:
    :param loan_id:
    :param start_date:
    :param loan_amount:
    :param annual_interest_rate:
    :param period_loan:
    :return:
    """
    user = get_object_or_404(User, id=user_id)

    loan = Loan.objects.filter(id=loan_id).first()

    monthly_interest_rate = float(
        (
            annual_interest_rate
            / NumberMonthOfYear.NUMBER_TWELFTH_MONTH_YEAR.value
        )
        / 100,
    )

    balance = loan_amount

    start_date = start_date + relativedelta(months=1)

    for _ in range(1, int(period_loan) + 1):
        interest = balance * monthly_interest_rate
        principal_payment = loan_amount / period_loan
        balance -= principal_payment
        monthly_payment = interest + principal_payment

        year = start_date.year
        month = start_date.month
        day = start_date.day
        current_date = datetime.date(year, month, day)

        next_date = start_date + relativedelta(months=1)

        PaymentSchedule.objects.create(
            user=user,
            loan=loan,
            date=current_date,
            balance=round(balance, 2),
            monthly_payment=round(monthly_payment, 2),
            interest=round(interest, 2),
            principal_payment=round(principal_payment, 2),
        )

        start_date = next_date
