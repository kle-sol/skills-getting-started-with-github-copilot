import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import activities, app


class UnregisterTests(unittest.TestCase):
    def setUp(self):
        self.activities_patch = patch.dict(
            activities,
            {
                "Chess Club": {
                    "participants": ["student+test@example.com", "other@example.com",
                                     "student+test@example.com"]
                }
            },
            clear=True,
        )
        self.activities_patch.start()
        self.addCleanup(self.activities_patch.stop)
        self.client = TestClient(app)

    def test_unregister_removes_all_matching_entries_and_allows_signup_again(self):
        params = {"email": "student+test@example.com"}
        response = self.client.delete("/activities/Chess%20Club/signup", params=params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(activities["Chess Club"]["participants"], ["other@example.com"])
        self.assertEqual(
            self.client.post("/activities/Chess%20Club/signup", params=params).status_code,
            200,
        )

    def test_unknown_activity_or_participant_returns_404(self):
        params = {"email": "missing@example.com"}
        self.assertEqual(
            self.client.delete("/activities/Missing/signup", params=params).status_code,
            404,
        )
        self.assertEqual(
            self.client.delete("/activities/Chess%20Club/signup", params=params).status_code,
            404,
        )
        self.assertEqual(len(activities["Chess Club"]["participants"]), 3)


if __name__ == "__main__":
    unittest.main()
