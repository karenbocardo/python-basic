from src import task_3

def test_url():
    assert task_3.is_http_domain('http://wikipedia.org') == True

def test_url_with_slash():
    assert task_3.is_http_domain('https://ru.wikipedia.org/') == True

def test_grid():
    assert task_3.is_http_domain('griddynamics.com') == False