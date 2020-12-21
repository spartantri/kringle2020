# CAN-Bus Investigation
Welcome to the CAN bus terminal challenge!

In your home folder, there's a CAN bus capture from Santa's sleigh. Some of
the data has been cleaned up, so don't worry - it isn't too noisy. What you
will see is a record of the engine idling up and down. Also in the data are
a LOCK signal, an UNLOCK signal, and one more LOCK. Can you find the UNLOCK?
We'd like to encode another key mechanism.

Find the decimal portion of the timestamp of the UNLOCK code in candump.log
and submit it to ./runtoanswer!  (e.g., if the timestamp is 123456.112233,
please submit 112233)

## Solution
The candump.log has many events but there are only three different ID in it.
```
elf@e9d6693bd207:~$ awk '{print $NF}' candump.log |cut -d\# -f1 |sort |uniq -c 
     35 188
      3 19B
   1331 244
```
Also those with id `19B` are longer than the rest, so simple grep using a regular expression to filter the events with at least 11 characters will yield the `LOCK` and `UNLOCK` events that can also be confirmed in the Santa Sleigh. 
```
elf@e9d6693bd207:~$ egrep '#.{11}' candump.log 
(1608926664.626448) vcan0 19B#000000000000
(1608926671.122520) vcan0 19B#00000F000000
(1608926674.092148) vcan0 19B#000000000000
```
As per the instructions there are one `LOCK`, followed by the `UNLOCK` and another `LOCK` after that, so this make easy to identify that `122520` is the answer.
```
elf@e9d6693bd207:~$ ./runtoanswer 
There are two LOCK codes and one UNLOCK code in the log.  What is the decimal portion of the UNLOCK timestamp?
(e.g., if the timestamp of the UNLOCK were 1608926672.391456, you would enter 391456.
> 122520
Your answer: 122520

Checking....
Your answer is correct!
```