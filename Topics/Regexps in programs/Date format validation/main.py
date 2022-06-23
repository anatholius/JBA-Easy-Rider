import re


def research(string):
    """
    Function restricted between 1800 <= t < 2099
    """

    return re.search(r"""
        (
            (0[1-9]|[12]\d|3[01])  # day 01-09 | 10-29 | 30-31 
            /  # separator
            (0[13578]|1[02])  # month (01,03,05,07,08) | (10,12)
            /  # separator
            (18|19|20)\d{2}  # year 1800-2099
        )  # 31 days long month
        |
        (
            (0[1-9]|[12]\d|30)  # day 01-09 | 10-29 | 30
            /  # separator
            (0[469]|11)  # month (04,06,09,11)
            /  # separator
            (18|19|20)\d{2}  # year 1800-2099
        )  # 30 days long month
        |
        (
            (0[1-9]|1\d|2[0-8])  # day 01-09 | 10-19 | 20-28
            /  # separator
            (02)  # month 02
            /  # separator
            (18|19|20)\d{2}  # year 1800-2099
        )  # 28 days long February
        |
        (
            29  # day 29
            /  # separator
            (02)  # month 02
            /  # separator
            (
                (
                    (18|19|20)(04|08|[2468][048]|[13579][26])
                )  # leapyears between 1804 and 2096 
                |  # or
                2000  # millenium
            )  # leapyear
        )  # 29 days long February
    """, string, flags=re.X)


def validate_date(string):
    # match = string and research(string) or ''
    # print(f' match: "{match}", string: "{string}" ')
    # print(match and match.groups() or 'No match')

    print(bool(string and research(string)))


# validate_date('01/12/2018')  # True
# validate_date('39/19/2020')  # False
# validate_date('01/12/0000')  # False
# validate_date('29/02/1800')  # False
# validate_date('01/01/2100')  # False - restriction 1800 <= t < 2099
# validate_date('29/02/2100')  # False - not valid but also restricted here
# validate_date('16/12/2020')  # True
validate_date(input())
