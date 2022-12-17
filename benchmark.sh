#!/usr/bin/env bash

# U=1
P=10

for U in 10 20 30 40 50 60 70 80 90 100
do
    echo "`date` U = $U, P = $P start"
    ./main.py -u $U -p $P &> log/${U}U_${P}P.log
    echo "`date` U = $U, P = $P end"
done