CUSTOMER_STATUS_CHOICES = ((1, "Active"), (2, "Inactive"))

customer_status_dict = dict(map(reversed, CUSTOMER_STATUS_CHOICES))


LOAN_STATUS_CHOICES = (
    (1, "Pending"),
    (2, "Active"),
    (3, "Rejected"),
    (4, "Paid"),
)

loan_status_dict = dict(map(reversed, LOAN_STATUS_CHOICES))

PAYMENT_STATUS_CHOICES = (
    (1, "Completed"),
    (2, "Rejected"),
)

payment_status_dict = dict(map(reversed, PAYMENT_STATUS_CHOICES))
