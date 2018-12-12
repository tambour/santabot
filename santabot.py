'''
secret santa matchmaker!

email: kaliszewskisanta@gmail.com

NOTICE: always matches Bret and Brennan
'''

import sys
import random
import time
import traceback
from smtplib import SMTP_SSL as SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def main():

    # make list of families
    families = \
    [
        Family('Grandma', \
        [
            Member('Ginger', '*******@**.**.com')
        ]),
        Family('Asadorians', \
        [
            Member('Kevan', '*****.*********@*****.com'),
            Member('Susie', '**************@*****.com'),
            Member('Nick',  '*********.****@*****.com'),
            Member('Adam',  '****.*********@*****.com'),
            Member('Bret',  '*************@*****.com')
        ]),
        Family('Kaliszewskis', \
        [
            Member('Don',     '************@***.com'),
            Member('Amanda',  '**************@**.com'),
            Member('Oisin',   '****************@*****.com'),
            Member('Brennan', '******************@*****.com')
        ]),
        Family('Whites', \
        [
            Member('Monica', '**********@*****.com'),
            Member('Ashley', '*****.********@*****.com'),
            Member('Kara',   '*************@*****.com'),
            Member('Danny',  '******@*****.com'),
            Member('Chris',  '***************@*****.com'),
            Member('Jay',    '***********@*******.com')
        ]),
    ]

    # always match bret / brennan
    families[1].members[4].choice = families[2].members[3]
    families[2].members[3].choice = families[1].members[4]
    families[1].members[4].chosen = True
    families[2].members[3].chosen = True


    # loop until everyone has been chosen
    while True:

        # find a giver
        family = get_random_family(families)
        member = get_random_member(family)

         # find another family
        other_family = get_other_family(families, family)
        if not other_family:
            # deadlock, start over
            main()
            return

        # find a recipient
        member.choice = other_family.get_member()

        # done if everyone has a match
        all_matched = True
        for family in families:
            for member in family.members:
                if not member.choice:
                    all_matched = False
                    continue

        if all_matched:
            break


    # done, print results / write to file
    f = open('santabot_lastrun.txt', 'w')
    for family in families:
        #print('{}'.format(family.name))
        f.write('{}\n'.format(family.name))
        for member in family.members:
            #print('    {}\t->\t{}'.format(member.name.ljust(7), member.choice.name))
            f.write('    {}\t->\t{}\n'.format(member.name.ljust(7), member.choice.name))
    f.close()


    # email everyone
    for family in families:
        for member in family.members:

            # connect to smtp server
            connected = False
            try:
                # please don't use your real gmail
                s = open('creds.txt', 'r')
                sender = s.readline()
                pw = s.readline()
                smtp_server = SMTP('smtp.gmail.com','465')
                smtp_server.login(sender, pw)
                connected = True
            except:
                traceback.print_exc()
                sys.exit(0)

            # construct the message
            if connected:
                message = \
                        'Hi {}, you have {} for Secret Santa!\n\n'.format(member.name, member.choice.name) + \
                        'Here is {}\'s wish list:\n'.format(member.choice.name) + \
                        '"'+member.choice.wishlist+'"' + '\n\n' + \
                        '(Sorry for the late start! We can get everyone\'s wishlists at Thanksgiving next year.\n' + \
                        'If you have any questions for {}, reply to this email and I\'ll relay them anonymously.\n'.format(member.choice.name) + \
                        'Source code here: https://github.com/tambour/santabot)\n\n' + \
                        'Merry Christmas!\n'
                msg = MIMEText(message)
                msg['Subject'] = 'Secret Santa for {}'.format(member.name)
                msg['From'] = sender
                msg['To'] = member.email

                try:
                    # send the message (switch commented line for test/prod)
                    smtp_server.sendmail(sender, [sender], msg.as_string()) # TEST
                    #smtp_server.sendmail(sender, [member.email], msg.as_string()) # ACTUAL
                    print('sent email to {}, ({})'.format(member.name, member.email))
                except SMTPException as e:
                    print('error sending to {}:'.format(member.name))
                    traceback.print_exc()
                finally:
                    s.close()
                    smtp_server.close()


class Family:

    def __init__(self, name, members):
        self.name = name
        self.members = members
        self.all_chosen = False

    def get_member(self):
        '''
        find unchosen family member
        '''
        member = random.sample(self.members, 1)[0]
        while member.chosen:
            member = random.sample(self.members, 1)[0]

        member.chosen = True
        self.check_all_chosen()

        return member

    def check_all_chosen(self):
        '''
        determine whether all family members chosen
        '''
        all_chosen = True
        for member in self.members:
            if not member.chosen:
                all_chosen = False
                break

        if all_chosen:
            self.all_chosen = True


class Member:
    def __init__(self, name, email, wishlist=''):
        self.name = name
        self.email = email
        self.wishlist = wishlist
        self.choice = None
        self.chosen = False


def get_random_family(families):
    '''
    select a random family with at least
    one member who does not have a match
    '''
    found = False
    while not found:

        for i in range(random.randint(1, 256)):
            family = random.sample(families, 1)[0]

        for member in family.members:
            if not member.choice:
                found = True

    return family

def get_random_member(family):
    '''
    select a random family member without a match
    '''
    found = False
    while not found:

        for i in range(random.randint(1, 256)):
            member = random.sample(family.members, 1)[0]

        if not member.choice:
            found = True

    return member

def get_other_family(families, family):
    '''
    get other family with at least
    one member who has not been chosen

    possible to run out of options,
    so there's a one second timeout
    '''

    start_time = time.time()

    found = False
    while not found:

        for i in range(random.randint(1, 256)):
            other_family = random.sample(families, 1)[0]

        if other_family.name != family.name:
            for member in other_family.members:
                if not member.chosen:
                    found = True

        if time.time() > start_time + 1:
            return None

    return other_family


if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
