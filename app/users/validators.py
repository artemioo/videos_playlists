from email_validator import EmailNotValidError, validate_email as validate_email_lib


def _validate_email_util(email):
    msg = ""
    valid = False
    try:
        valid = validate_email_lib(email)
        # update the email var with a normalized value
        email = valid.email
        valid = True
    except EmailNotValidError as e:
        msg = str(e)
    return valid, msg, email
