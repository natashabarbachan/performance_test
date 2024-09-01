import time
from locust import HttpUser, task, between, constant, events

HttpUser.host = 'https://fakerestapi.azurewebsites.net/api/v1'

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print('Starting Tests...')

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print('Finishing Tests...')

def verifyResponseStatusCode(response):
    if response.status_code == 200:
        print('Test Passed')
    else:
        response.failure("Test Failed")
    print('Status Code: ', response.status_code)
    print('Body: ', response.text)

# Task created outside the User class
def getAllBooks(self):
    with self.client.get('/Books', catch_response = True) as response:
        verifyResponseStatusCode(response)

class RegularUser(HttpUser):
    weight = 3
    wait_time = between(1,5)
    tasks = { getAllBooks: 3 }

    @task(2)
    def getBook(self):
        for item_id in range(1, 10):
            with self.client.get(f'/Books/{item_id}', name='/Books/item_id', catch_response = True) as response:
                verifyResponseStatusCode(response)
            time.sleep(1)

    def on_start(self):
        self.client.get('/Users/2')
        print('ON START EXECUTED FOR REGULAR USER')

    def on_stop(self):
        self.client.get('/Users/2')
        print('ON STOP EXECUTED FOR REGULAR USER')

class AdminUser(HttpUser):
    fixed_count = 2
    wait_time = constant(5)
    tasks = { getAllBooks: 1 }

    @task(2)
    def postBook(self):
        payload = {
            'id': 1,
            'title': 'O Enigma do Tempo',
            'description': 'Um romance fascinante que explora a vida de uma jovem cientista.',
            'pageCount': 100,
            'excerpt': 'Naquela noite, ela sabia que, com um único movimento, poderia mudar tudo ou destruir tudo.',
            'publishDate': '2024-09-01T16:53:36.081Z'
        } 

        with self.client.post('/Books', json = payload, catch_response = True) as response:
            verifyResponseStatusCode(response)

    def on_start(self):
        self.client.get('/Users/1')
        print('ON START EXECUTED FOR ADMIN USER')

    def on_stop(self):
        self.client.get('/Users/1')
        print('ON STOP EXECUTED FOR ADMIN USER')