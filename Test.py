duty_cyrcle = (0.39, 0.7, 0.4, 0.21, 0.99, 0.03, 0.08)

number_of_clk_part = [num * 32 for num in duty_cyrcle]

for item in range(len(duty_cyrcle)):
    print('Duty cycle={}    |Width of pulse={}'.format(duty_cyrcle[item]*100, number_of_clk_part[item]))


print('-' * 10)

for i in range(1, 33):
    print('{}/32={}%'.format(i, i / 32*100))

print('-' * 10)

out_pulse_width = (13, 22, 13, 7, 32, 1, 3)

for i, item in enumerate(out_pulse_width):
    print('out[{0}]={1}={2}'.format(i, item, bin(item)))
