from datetime import datetime
from typing import Optional

from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet
from hasta_la_vista_money.budget.models import DateList
from hasta_la_vista_money.constants import NumberMonthOfYear
from hasta_la_vista_money.users.models import User


def generate_date_list(
    current_date: Optional[datetime, QuerySet],
    user: User,
):
    """Функция генерации первых 12 месяцев начиная с переданной даты."""
    if isinstance(current_date, datetime):
        current_date = current_date.date()

    if isinstance(current_date, QuerySet):
        current_date = current_date.last().date

    list_date = [
        current_date + relativedelta(months=date_index)
        for date_index in range(
            0,
            NumberMonthOfYear.NUMBER_TWELFTH_MONTH_YEAR.value + 1,
        )
    ]

    for item_date in list_date:
        date_list_instance = DateList(user=user, date=item_date)
        date_list_instance.save()
