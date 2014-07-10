#!/bin/sh

tail -n +2 PLZ.tab | awk -F"\t" '{print "- model: services.location\n  pk: "FNR"\n  fields:\n    plz: "$2"\n    lon: "$3"\n    lat: "$4"\n    name: "$5}' > initial_data.yaml

