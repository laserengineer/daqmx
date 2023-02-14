import pprint
import nidaqmx
from nidaqmx.constants import TerminalConfiguration

pp = pprint.PrettyPrinter(indent=4)


with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=TerminalConfiguration.RSE, min_val=-5)
 
    print('1 Channel 1 Sample Read: ')
    data = task.read()
    pp.pprint(data)

    data = task.read(number_of_samples_per_channel=1)
    pp.pprint(data)

    print('1 Channel N Samples Read: ')
    data = task.read(number_of_samples_per_channel=8)
    pp.pprint(data)

    task.ai_channels.add_ai_voltage_chan("Dev1/ai1:3")

    print('N Channel 1 Sample Read: ')
    data = task.read()
    pp.pprint(data)

    print('N Channel N Samples Read: ')
    data = task.read(number_of_samples_per_channel=2)
    print(data)