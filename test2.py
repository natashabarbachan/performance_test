import time
from unicodedata import name
from locust import HttpUser, task, between, constant

class LibraryRegularUser(HttpUser):
    weight = 3
    wait_time = between(2,6)
    host = "https://fakerestapi.azurewebsites.net/api/v1"

    @task
    def readActivitiesAuthors(self):
        self.client.get('/Activities')
        self.client.get('/Authors')

    @task(2)
    def getActivity(self):
        for item_id in range(1, 11):
            self.client.get(f'/Activities/{item_id}', name='/Activities/item_id') 
            time.sleep(1)

    def on_start(self): # É executado apra cada user instanciado 
        self.client.get('/Users/5')
        print('ON START EXECUTED')


class LibraryRareUser(HttpUser):
    fixed_count = 2
    wait_time = constant(5)
    host = "https://fakerestapi.azurewebsites.net/api/v1"

    @task
    def deleteActivity(self):
        self.client.delete('/Activities/8')

    def on_stop(self): # É executado apra cada user instanciado 
        self.client.delete('/Users/5')
        print('ON STOP EXECUTED')
    


