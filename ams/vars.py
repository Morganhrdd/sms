HOLIDAY_RULE='Holiday'

DAY_CHOICES = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
)

MONTH_CHOICES = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)

REMARK_CHOICES = (
	('A', 'Absent'),
	('P', 'Present'),
	('L', 'Late'),
	('E', 'EarlyOut'),
	('H', 'HalfDay'),
	('O', 'Leave'),
	('C', 'Compensatory Off'),
	('S', 'Holiday'),
	('D', 'OnDuty'),
	('F', 'Approved HalfDay'),
)

STATUS_CHOICES = (
	('I', 'In'),
	('O', 'Out'),
        ('T', 'Termination'),
)

LEAVE_CHOICES = (
	(1, 'Casual'),
	(2, 'Sick'),
	(3, 'Earned'),
	(4, 'OnDuty(First)'),
	(5, 'Halfday(First)'),
	(6, 'Halfday(Second)'),
	(7, 'OnDuty(Second)'),
)

LEAVESTATUS_CHOICES = (
	(1, 'Pending'),
	(2, 'Approve'),
	(3, 'Deny'),
	(4, 'Pending Deny'),
)

YEAR_CHOICES = (
	(1, 'Current'),
	(2, 'Other'),
)

FORGOT_CHECKOUT_CHOICES = (
	(1, 'Update Attendance'),
	(2, 'Done'),
)

