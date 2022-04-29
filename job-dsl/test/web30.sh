#!/bin/bash
url='https://10.10.33.5/flask'
attempts=2
timeout=2
online=false

echo "Checking status of $url."
echo "Checking status of $timeout."
echo ${TIMEOUT}

for (( i=1; i<=$attempts; i++ ))
do
  code=`curl -sL --connect-timeout 2 --max-time 3 -w "%{http_code}\\n" "$url" -o /dev/null`

  echo "Found code $code for $url."

  if [ "$code" = "200" ]; then
    echo "Website $url is online."
    online=true
    break
  else
    echo "Website $url seems to be offline. Waiting $timeout seconds."
    sleep $timeout
  fi
done

if $online; then
  echo "Monitor finished, website is online."
  exit 0
else
  echo "Monitor failed, website seems to be down."
  exit 1
fi
