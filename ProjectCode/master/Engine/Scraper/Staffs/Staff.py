"""
Generating a Staff object, getting scrapping result and saving the object by calling output function

Authors:
- Leyang Chai u7201445
"""

class Staff(object):
    def __init__(self, email, name, attributes={}):
        '''
        :param email: str email address for staff
        :param name:
        :param attributes {
            'university':university,
            'phone':phone,
            'Project':project,
            'Title':title=None,
            'Interests':interests=None,
            'BioText':bioText,
            }
        '''
        self.email = None
        self.name = None
        self.otherEmails = None
        self.university = None
        self.colleges = None
        self.title = None

        self.profile = None
        self.staffTags = None
        self.projectTags = None

        if len(email) != 0: self.email = email[0]
        self.name = name
        self.otherEmails = '<bk>'.join(i for i in email[1:])

        try:
            self.university = attributes.get('University')
            self.colleges = attributes.get('Colleges')
            self.title = attributes.get('Title')
            self.profile = attributes.get('Profile')
            self.staffTags = attributes.get('staffTags')
            self.projectTags = attributes.get('ProjectTags')

        except Exception as e:
            raise e

    def output(self):

        return {
            'Name': self.name,
            'Email': self.email,
            'OtherEmails': self.otherEmails,
            'University': self.university,
            'Colleges': self.colleges,
            'Title': self.title,
            'Profile': self.profile,
            'staffTags': '<bk>'.join(k + '<weight>' + v for k, v in self.staffTags.items()),
            'ProjectTags': '<bk>'.join(k + '<weight>' + v for k, v in self.projectTags.items()),
        }

    def resetEmail(self, email):
        self.email = email

    def verifyEmail(self, email):
        import re
        # email='hendra.gunadi@anu.edu.au'
        pattern = r'^.+@[0-9a-zA-Z]{1,13}\.([a-zA-Z]{1,10}\.*)+$'
        if re.match(pattern, email) is not None:
            return True
        else:
            return False

    def getEmail(self):
        return self.email

    def getName(self):
        return self.name

    def getInterests(self):
        return self.interests
