## django_test_app

Django test project

#### Endpoints:
- `/api/docs/ Swagger UI`
- `admin/ Django admin`
- `/api/token/ {"username": "string", "password": "string"} Generate JWT use Swagger`


#### 🔧 Build: 
```commandline 
docker compose build app
docker compose run app python manage.py migrate
docker compose run app python manage.py createsuperuser
```

#### 🕵️‍♀️ Test: 
```commandline
docker compose run app pytest
```

#### 🟢 Run: 
```commandline
docker compose up app -d
```


### Bench 
change create object count `bench.py:69`
```python
    asyncio.run(main(cnt=1000))
```
```commandline 
docker compose run app python -m gunicorn settings.wsgi:application --workers 10 --log-level debug
```
```commandline 
uv run python bench.py 
```
