
install poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```


clone repo
```bash
git clone https://github.com/mszpulak/appic.git
```

run server:
```bash
./manage.py runserver
```

# Adding Updating Objects (can be using rendered RestApi Web)

list event:
```bash
http://127.0.0.1:8000/api/event/
```

add event  -> POST:
```bash
http://127.0.0.1:8000/api/event/
```

update event - GET and PUT: 
```bash
http://127.0.0.1:8000/api/event/2/
```

getting sorted enents with perf: 
```bash
http://127.0.0.1:8000/api/event_perf/?ordering=-start
http://127.0.0.1:8000/api/event_perf/?ordering=start
```
creating new performance with event and artist:

```bash
curl --header "Content-Type: application/json" --request POST --data 
' {
    "event": "aaaa",
    "artist": [
        "aaaaa",
        "ddddd"
    ],
    "start": "2024-05-18T14:44:56Z",
    "end": "2024-05-18T14:44:57Z"
}' http://127.0.0.1:8000/api/performance/
```
```bash
curl --header "Content-Type: application/json" --request PUT --data 
' {
    "event": "aaaa",
    "artist": [
        "aaaaa",
        "ddddd"
    ],
    "start": "2024-05-11T14:44:56Z",
    "end": "2024-05-11T14:44:57Z"
}' http://127.0.0.1:8000/api/performance/5/
```


download CSV
```bash
http://127.0.0.1:8000/api/event/?format=csv
```

