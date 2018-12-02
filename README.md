# santabot
- Randomly matches everyone with someone outside of their immediate family
- Emails everyone with their recipient's name and wishlist

## Usage
1. Populate the `families` list described below
2. run `python santabot.py`

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