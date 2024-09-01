import time
from locust import HttpUser, task, between, constant, events

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print('Starting Tests')

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print('Finishing Tests')

# Tasks declaradas fora das classes dos users
def readActivitiesAuthors(self):
    response = self.client.get('/Activities')
    print('Status Code: ', response.status_code)
    print('Body: ', response.text)

    self.client.get('/Authors')
    print('Status Code: ', response.status_code)
    print('Body: ', response.text)

def getActivity(self):
    for item_id in range(1, 11):
        response = self.client.get(f'/Activities/{item_id}', name='/Activities/item_id') 
        print('Status Code: ', response.status_code)
        print('Body: ', response.text)
        time.sleep(1)

def deleteActivity(self):
    with self.client.delete('/Activities/8', catch_response = True) as response:
        if response.status_code == 200:
            response.failure("Test Failed")
        print('Status Code: ', response.status_code)
        print('Body: ', response.text)


class LibraryRegularUser(HttpUser):
    weight = 3
    wait_time = between(2,6)
    host = "https://fakerestapi.azurewebsites.net/api/v1"
    tasks = { readActivitiesAuthors: 2, getActivity: 1 }

    def on_start(self): # É executado apra cada user instanciado 
        self.client.get('/Users/5')
        print('ON START EXECUTED')


class LibraryRareUser(HttpUser):
    fixed_count = 2
    wait_time = constant(5)
    host = "https://fakerestapi.azurewebsites.net/api/v1"
    tasks = { readActivitiesAuthors: 1, deleteActivity: 3 }

    def on_stop(self): # É executado apra cada user instanciado 
        self.client.delete('/Users/5')
        print('ON STOP EXECUTED')
    


