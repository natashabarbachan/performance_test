from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1,5)
    host = 'http://fakerestapi.azurewebsites.net'

    @task 
    def index(self):
        self.client.get('/api/v1/Activities')
