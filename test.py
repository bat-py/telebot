uzcard = str(1234123412341234)
# nice_uzcard = f'{uzcard[0:4]} {uzcard[0:4]} {uzcard[0:4]} {uzcard[0:4]} '
nice_uzcard = [f"{uzcard[i:i+4]}" for i in range(0,16, 4)]
nice_uzcard = ' '.join(nice_uzcard).strip()
print(nice_uzcard)