# santabot
- Randomly matches everyone with someone outside of their immediate family
- Emails everyone with their recipient's name and wishlist

## Usage
1. Make a throwaway gmail account
2. Put gmail username/password in creds.txt
3. Populate the `families` list described below
4. run `python santabot.py`

## Family Structure
```
families = \
[
    Family('Johnsons', \
    [
        #      Name:    Email:              Wishlist:
        Member('Pappy', 'pappyj@gmail.com', 'whiskey'),
        ...
    ]),
    ...
]
```