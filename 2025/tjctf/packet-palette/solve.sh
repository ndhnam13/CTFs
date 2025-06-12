#!/bin/bash

tshark -r chall.pcapng -T fields -e data | grep -o '0001f4.*' | sed 's/0001f4//' > png.txt

xxd -r -p png.txt > real.png