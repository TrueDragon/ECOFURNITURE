# User class
class Report:
    report_id = 0
    
    # initializer method
    def __init__(self, email, issue, remarks):
        Report.report_id += 1
        self.__email = email
        self.__issue = issue
        self.__remarks = remarks

    # accessor methods
    def get_email(self):
        return self.__email

    def get_issue(self):
        return self.__issue

    def get_remarks(self):
        return self.__remarks

    # mutator methods
    def set_email(self, email):
        self.__email = email

    def set_issue(self, issue):
        self.__issue = issue

    def set_remarks(self, remarks):
        self.__reamrks = remarks
