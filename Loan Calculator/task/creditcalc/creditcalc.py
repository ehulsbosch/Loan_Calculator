import math
import argparse
import numbers

parser = argparse.ArgumentParser(description='Calculating loan variables')
parser.add_argument('--principal', dest='principal', type=int)
parser.add_argument('--periods', dest='periods', type=int)
parser.add_argument('--interest', dest='interest', type=float)
parser.add_argument('--payment', dest='payment', type=int)
parser.add_argument('--type', dest='type', type=str, choices=['annuity', 'diff'])


def evaluate_arguments(a):
    # if len(a.__dict__) != 5:
    #     exit('Incorrect parameters')
    numberofnones = 0
    if a.type not in ('annuity', 'diff'):
        print('Incorrect parameters')
    if a.type == 'diff' and a.payment is not None:
        print('Incorrect parameters')
    if a.type == 'annuity' and a.interest is None:
        print('Incorrect parameters')
    for attr, value in a.__dict__.items():
        if isinstance(value, (int, float)) and value < 0:
            print('Incorrect parameters')
        if value == None:
            numberofnones = numberofnones + 1
            if numberofnones > 1:
                print('Incorrect parameters')


try:
    parsed_args = parser.parse_args()
    evaluate_arguments(parsed_args)
except argparse.ArgumentError:
    exit('Parsing error')


def months_to_years(m: float) -> (int, int):
    years = math.floor(m / 12)
    months = m % 12
    return years, months


def calc_overpayment(principal: float, periods: float, annuity: float) -> int:
    return int((periods * math.ceil(annuity)) - principal)


def calculate_monthly_interest(interest: float) -> float:
    return (interest / 100) / 12


# Calculates the months necessary to pay off the loan. Only full months supported
def calc_months(principal: float, payment: float, interest: float) -> (int, int):
    i = calculate_monthly_interest(interest)
    calculated_months = math.log(payment / (payment - i * principal), 1 + i)
    final_months = math.ceil(calculated_months)
    overpayment = calc_overpayment(principal, final_months, payment)
    years, months = months_to_years(final_months)
    if years == 0:
        print(f'It will take {months} months to repay this loan!')
    elif months == 0:
        print(f'It will take {years} years to repay this loan!')
    else:
        print(f'It will take {years} years and {months} months to repay this loan!')
    print(f'Overpayment = {overpayment}')
    return years, months


def calculate_annuity(principal: float, period: float, interest: float) -> int:
    i = calculate_monthly_interest(interest)
    annuity = principal * (
        i * (1 + i) ** period
    ) / (
        (1 + i) ** period - 1
    )
    overpayment = calc_overpayment(principal, period, annuity)
    # overpayment = math.ceil(math.ceil(annuity) * period) - principal
    print(f'Your annuity payment = {math.ceil(annuity)}!')
    print(f'Overpayment = {overpayment}')
    return int(math.ceil(annuity))


def calculate_loan_principal(annuity: float, periods: float, interest: float) -> int:
    i = calculate_monthly_interest(interest)
    principal = annuity / (
        (i * (1+i) ** periods) / ((1+i)**periods - 1)
    )
    overpayment = calc_overpayment(principal, periods, annuity)
    print(f'Your loan principal = {int(principal)}!')
    print(f'Overpayment = {overpayment}')
    return int(principal)


# Calculates the monthly payments necessary to pay off the loan. Only integers supported
def calc_payments(principal: float, months_to_pay: float) -> (int, int):
    calculated_monthly_sum = principal / months_to_pay
    if isinstance(calculated_monthly_sum, int):
        return int(calculated_monthly_sum), None
    else:
        new_monthly_sum = int(math.ceil(calculated_monthly_sum))
        last_payment = int(principal - (months_to_pay - 1) * new_monthly_sum)
        return new_monthly_sum, last_payment


def calculate_differentiate_payments(principal: float, periods: float, interest: float,  month_number: int = None):
    i = calculate_monthly_interest(interest)
    month = 1
    sum_payments = 0
    while month <= periods:
        raw_payment = (principal / periods) + i * (
            principal - ((principal * (month - 1)) / periods)
        )
        payment = math.ceil(raw_payment)
        sum_payments = sum_payments + payment
        print('Month {}: payment is {}'.format(month, payment))
        month = month + 1

    overpayment = sum_payments - principal
    print('Overpayment = {}'.format(overpayment))


if parsed_args.type == 'diff' and parsed_args.principal is not None and parsed_args.periods is not None and parsed_args.interest is not None:
    calculate_differentiate_payments(parsed_args.principal, parsed_args.periods, parsed_args.interest)
if parsed_args.type == 'annuity' and parsed_args.principal is not None and parsed_args.payment is not None and parsed_args.interest is not None:
    val = calc_months(parsed_args.principal, parsed_args.payment, parsed_args.interest)
if parsed_args.type == 'annuity' and parsed_args.principal is not None and parsed_args.periods is not None and parsed_args.interest is not None:
    val = calculate_annuity(parsed_args.principal, parsed_args.periods, parsed_args.interest)
if parsed_args.type == 'annuity' and parsed_args.payment is not None and parsed_args.interest is not None and parsed_args.periods is not None:
    val = calculate_loan_principal(parsed_args.payment, parsed_args.periods, parsed_args.interest)

#
#
# def get_loan_principal() -> float:
#     return float(input('Enter the loan principal:\n'))
#
#
# def get_loan_interest() -> float:
#     return float(input('Enter the loan interest:\n'))
#
#
# def get_loan_periods() -> float:
#     return float(input('Enter the number of periods: \n'))
#
#
# def receive_manual_input():
#     type_of_calculation = input('What do you want to calculate? \n'
#                             'type "n" for number of monthly payments, \n'
#                             'type "a" for annuity monthly payment amount, \n'
#                             'type "p" for loan principal: \n')
#
#     if type_of_calculation == 'n':
#         loan_principal = get_loan_principal()
#         monthly_payment = float(input('Enter the monthly payment:\n'))
#         interest = get_loan_interest()
#         years, months = calc_months(loan_principal, monthly_payment, interest)
#         month_string = 'months' if months != 1 else 'month'
#         print('It will take {} years and {} to repay this loan!'.format(years, months))
#
#     elif type_of_calculation == 'a':
#         loan_principal = get_loan_principal()
#         periods = get_loan_periods()
#         interest = get_loan_interest()
#         annuity = calculate_annuity(loan_principal, periods, interest)
#         print('Your monthly payment = {}'.format(annuity))
#
#     elif type_of_calculation == 'p':
#         annuity_payment = float(input('Enter the annuity payment: \n'))
#         periods = get_loan_periods()
#         interest = get_loan_interest()
#
#         loan_principal = calculate_loan_principal(annuity_payment, periods, interest)
#         print('Your loan principal = {}'.format(loan_principal))
#
#
# if parsed_args is None:
#     receive_manual_input()
# if parsed_args.type == 'diff':