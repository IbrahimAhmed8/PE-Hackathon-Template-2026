from locust import HttpUser, task, between

class HackathonStressTest(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def test_health_and_list(self):
        self.client.get("/health")
        self.client.get("/products")

    @task(1)
    def test_rasp_defense(self):
        self.client.post("/products", json={"name": "<script>alert('hack')</script>", "price": 10})
