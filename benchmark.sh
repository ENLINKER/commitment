#!/usr/bin/env bash

U=(10 10 100 100)
P=(10 100 10 100)

# for U in 10 20 30 40 50 60 70 80 90 100
# for U in 100 200 300 400 500 600 700 800 900 1000
for i in ${!U[@]}
do
    echo "`date` U = ${U[i]}, P = ${P[i]} start"
    ./main.py -u ${U[i]} -p ${P[i]} &> log/${U[i]}U_${P[i]}P.log
    echo "`date` U = ${U[i]}, P = ${P[i]} end"
done

git add .
git commit -m "new benchmark"
git push