#!/bin/bash
attempts=2
timeout=2
online=false

echo "Checking status of ${URL}."

for (( i=1; i<=$attempts; i++ ))
do
  code=`curl -sL -o /dev/null -k --connect-timeout 2 --max-time 3 -w "%{http_code}\\n" "${URL}"`

  echo "Found code $code for ${URL}."

  if [ "$code" = "200" ]; then
    echo "Website $url is online."
    online=true
    break
  else
    echo "Website ${URL} seems to be offline. Waiting $timeout seconds."
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
