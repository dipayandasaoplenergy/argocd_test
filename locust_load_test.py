from locust import HttpUser, task, between

class HealthCheckUser(HttpUser):
    wait_time = between(0.01, 0.05)
    host = "http://127.0.0.1:58193"
    host = "http://localhost:8000"

    def on_start(self):
        # Will run once when a simulated user starts
        r = self.client.get("/users")
        if r.status_code == 200:
            print("✅ Health endpoint working:", r.text)
        else:
            print("❌ Health check failed:", r.status_code, r.text)

    @task
    def check_health(self):
        self.client.get("/users")