#!/usr/bin/env bash


DATABASE='only-windows.db'


for file in "${@}"; do
    sqlite3 "${DATABASE}" < "${file}";
done
