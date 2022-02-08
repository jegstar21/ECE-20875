import re


def problem1(searchstring):
    """
    Match phone numbers.

    :param searchstring: string
    :return: True or False
    """
    # Choice One: XXX-XXXX format
    choice_one = re.findall("\d{3}[-]\d{4}", searchstring)

    # Choice Two: XXX-XXX-XXXX format
    choice_two = re.findall("\d{3}[-]\d{3}[-]\d{4}", searchstring)

    # Choice Three: (XXX)XXX-XXXX format
    choice_three = re.findall("\(\d{3}\)\d{3}[-]\d{4}", searchstring)

    # Choice Four: (XXX) XXX-XXXX format
    choice_four = re.findall("\(\d{3}\)\s\d{3}[-]\d{4}", searchstring)

    if len(searchstring) == 8 and len(choice_one) > 0:
        return True
    elif len(searchstring) == 12 and len(choice_two) > 0:
        return True
    elif len(searchstring) == 13 and len(choice_three) > 0:
        return True
    elif len(searchstring) == 14 and len(choice_four) > 0:
        return True
    else:
        return False

    pass


def problem2(searchstring):
    """
    Extract street name from address.

    :param searchstring: string
    :return: string
    """
    ####################˅˅˅˅˅˅˅˅ First Parentheses: Street Number
    #############################˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅ Second Parenthese: Street Name
    #################################################˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅ Third Parentheses: Street Type
    patternDetected = r"([0-9]+) (([A-Z]{1}[a-z]* )+)(Rd\.|Dr\.|Ave\.|St\.)"

    matchFound = re.search(patternDetected, searchstring)

    if matchFound:
        return matchFound.group(2)[:-1]
    return None


pass


def problem3(searchstring):
    """
    Garble Street name.

    :param searchstring: string
    :return: string
    """

    # Run the Street Name from Problem 2
    reversedName = problem2(searchstring)

    # Return with entire word reversed
    return re.sub(reversedName, reversedName[::-1], searchstring)


pass


if __name__ == "__main__":
    print(problem1("765-494-4600"))  # True
    print(problem1(" 765-494-4600 "))  # False
    print(problem1("(765) 494 4600"))  # False
    print(problem1("(765) 494-4600"))  # True
    print(problem1("494-4600"))  # True

    print(problem2("The EE building is at 465 Northwestern Ave."))  # Northwestern
    print(problem2("Meet me at 201 South First St. at noon"))  # South First

    print(problem3("The EE building is at 465 Northwestern Ave."))
    print(problem3("Meet me at 201 South First St. at noon"))
