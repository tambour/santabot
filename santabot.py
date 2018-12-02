'''
secret santa matchmaker!

email: kaliszewskisanta@gmail.com
       kaliszewskiclaus@gmail.com

NOTICE: always matches Bret and Brennan
'''

import sys
import random
import time
import traceback
from smtplib import SMTP_SSL as SMTP #SSL connection
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class Family:

    def __init__(self, name, members):
        self.name = name
        self.members = members
        self.all_chosen = False

    def get_member(self):
        '''
        find unchosen member
        '''
        member = random.sample(self.members, 1)[0]
        while member.chosen:
            member = random.sample(self.members, 1)[0]

        member.chosen = True
        self.check_all_chosen()

        return member

    def check_all_chosen(self):
        '''
        determine whether all members chosen
        '''
        all_chosen = True
        for member in self.members:
            if not member.chosen:
                all_chosen = False
                break

        if all_chosen:
            self.all_chosen = True

class Member:
    def __init__(self, name, email, wishlist):
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
    select a random member without a match
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


def main():

    # make list of families
    families = \
    [
        Family('Grandma', \
        [
            Member('Ginger',    'danbwh@gmail.com', 'wishlist')
        ]),
        Family('Asadorians', \
        [
            Member('Kevan',     'danbwh@gmail.com', 'wishlist'),
            Member('Susie',     'danbwh@gmail.com', 'wishlist'),
            Member('Nick',      'danbwh@gmail.com', 'wishlist'),
            Member('Adam',      'danbwh@gmail.com', 'wishlist'),
            Member('Bret',      'danbwh@gmail.com', \
                'Athletic shoes\n' + \
                'Vans\n' + \
                'Calvin Klein No shows\n' + \
                'Calvin Klein Boxers\n' + \
                'Retro basketball Jersey\n' + \
                'Chipotle gift card\n' + \
                'Sweatpants that get skinny toward ankle\n' + \
                'Express colored pants\n' + \
                'Long Nike socks black and white'
            )
        ]),
        Family('Kaliszewskis', \
        [
            Member('Don',       'danbwh@gmail.com', 'wishlist'),
            Member('Amanda',    'danbwh@gmail.com', 'wishlist'),
            Member('Oisin',     'danbwh@gmail.com', 'wishlist'),
            Member('Brennan',   'danbwh@gmail.com', 'wishlist')
        ]),
        Family('Whites', \
        [
            Member('Monica',    'danbwh@gmail.com', 'wishlist'),
            Member('Ashley',    'danbwh@gmail.com', 'wishlist'),
            Member('Kara',      'danbwh@gmail.com', \
                'I would love some cozy slippers (size 6 shoe), black leggings (XS), homage Ohio State sweatshirt (crew neck or hoodie, S), love your melon winter hat (any color), and sweaters (size XS or S, depending on where it\'s from)\n' + \
                'If anyone gets me homage here is a $20 off coupon!\n\nTLKF1018-107FA2B0'
            ),
            Member('Danny',     'danbwh@gmail.com', 'wishlist'),
            Member('Chris',     'danbwh@gmail.com', 'wishlist'),
            Member('Jay',       'danbwh@gmail.com', 'wishlist')
        ]),
    ]

    # always match bret / brennan
    families[1].members[4].choice = families[2].members[3]
    families[2].members[3].choice = families[1].members[4]
    families[1].members[4].chosen = True
    families[2].members[3].chosen = True



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

        # oisin armor
        if member.name == 'Oisin' and member.choice.name == 'Danny':
            # reroll
            member.choice = None
            continue

        # done if everyone has a match
        all_matched = True
        for family in families:
            for member in family.members:
                if not member.choice:
                    all_matched = False
                    continue

        if all_matched:
            break

    # done, print results
    f = open('santa.txt', 'w')
    for family in families:
        print('{}'.format(family.name))
        f.write('{}\n'.format(family.name))
        for member in family.members:
            print('    {}\t->\t{}'.format(member.name.ljust(7), member.choice.name))
            f.write('    {}\t->\t{}\n'.format(member.name.ljust(7), member.choice.name))
    f.close()


    # TODO: email everyone

    

    

    for family in families:
        for member in family.members:

            ServerConnect = False
            try:
                sender = 'kaliszewskisanta@gmail.com'
                smtp_server = SMTP('smtp.gmail.com','465')
                smtp_server.login('kaliszewskisanta@gmail.com', 'Touhou24')
                ServerConnect = True
            except:
                traceback.print_exc()
                sys.exit(0)

            if ServerConnect == True:

                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = member.email
                msg['Subject'] = 'Secret Santa'
                message = 'Hi {}, you have {} for secret santa!\n\n'.format(member.name, member.choice.name) + \
                          'The following is their wish list:\n' + \
                          member.choice.wishlist
                msg.attach(MIMEText(message))

                try:
                    smtp_server.sendmail(sender, [member.email], msg.as_string())
                    print "Successfully sent email"
                except SMTPException as e:
                    print "Error: unable to send email", e
                finally:
                    smtp_server.close()



if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print('ex: {}'.format(str(ex)))
