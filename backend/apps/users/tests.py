from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthFlowTest(APITestCase):
    def setUp(self):
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.me_url = "/api/users/me/"
        self.password_url = "/api/users/me/password/"
        self.profile_url = "/api/users/me/student-profile/"
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Test@12345",
            "password2": "Test@12345",
            "first_name": "Test",
            "last_name": "User",
            "role": "student"
        }

    def test_user_flow(self):
        # ✅ Register
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 201)

        # ✅ Login
        login = self.client.post(self.login_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password1"]
        })
        self.assertEqual(login.status_code, 200)

        # ✅ Extract and use token
        token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # ✅ Me endpoint
        res = self.client.get(self.me_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["username"], self.user_data["username"])

        # ✅ Change password
        pass_res = self.client.post(self.password_url, {
            "old_password": "Test@12345",
            "new_password": "New@12345"
        })
        self.assertEqual(pass_res.status_code, 200)

        # ✅ Set student profile
        prof_set = self.client.put(self.profile_url, {
            "bio": "Learner",
            "language_preference": "English",
            "education": "B.Tech",
            "interests": "AI, Web Dev",
            "learning_goals": "Become a full-stack dev",
            "budget_range": "₹5000-₹10000"
        })
        self.assertIn(prof_set.status_code, [200, 201])

        # ✅ Get student profile
        prof_get = self.client.get(self.profile_url)
        self.assertEqual(prof_get.status_code, 200)
        self.assertEqual(prof_get.data["language_preference"], "English")
