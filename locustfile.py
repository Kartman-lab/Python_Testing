from locust import HttpUser, task, between

class GudliftUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def view_index(self): 
        self.client.get("/")
    
    @task()
    def book_place(self):
        self.client.post("/purchasePlaces", {
            "club": "Iron Temple",
            "competition": "Spring Festival",
            "places": 2
        })

    @task
    def login_logout(self):
        self.client.post('/showSummary', {"email": "john@simplylift.co"})
        self.client.get("/logout")
