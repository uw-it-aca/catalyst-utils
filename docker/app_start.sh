#!/bin/bash

if [ "$ENV"  = "localdev" ]
then

  python manage.py migrate
  python manage.py loaddata test_data.json

fi
