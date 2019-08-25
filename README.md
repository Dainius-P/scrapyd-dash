# Scrapyd Dashboard

A dashboard specifically used for scrapyd servers to manipulate scrapy spiders (start, stop, check status).

### Features

- [x] Scrapyd server status
- [x] Tasks (add, remove, list)
- [x] Authentification (Using the Django authentication system)
- [ ] Scheduled tasks (add, remove, list)
- [ ] View logs
- [ ] Multiple independent user support
- [ ] Task performance details

### Demo

[Demo website](https://scrapyddash.herokuapp.com/)

Username: **demo**

Password: **demo**

### Installing

1. Install the package

```
pip install scrapyd_dash
```

2. Add urls to your projects urls.py

```
from django.urls import include

urlpatterns = [
    ...
    path('scrapyd_dash/', include('scrapyd_dash.urls')),
]

```


### Built With

* [Django](https://www.djangoproject.com/) - The web framework used.
* [ScrapyD](https://github.com/scrapy/scrapyd) - A service daemon to run Scrapy spiders.
* [LogParser](https://github.com/my8100/logparser) - A tool for parsing Scrapy log files.

### Authors

* **Dainius Preimantas** - *Initial work* - [Dainius-P](https://github.com/Dainius-P)

### Contributing

1. Fork it
2. Create your feature branch (```git checkout -b feature/fooBar```)
3. Commit your changes (```git commit -am 'Add some fooBar'```)
4. Push to the branch (```git push origin feature/fooBar```)
5. Create a new Pull Request


### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.