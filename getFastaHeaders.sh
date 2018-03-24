#!/bin/bash

awk '{if($1~/^>/){print $0}}' $1 > $1".headers"
