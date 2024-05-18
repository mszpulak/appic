from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import TaskReport, Performance
from model_mommy import mommy


class TaskTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data = {"content": "lorem ipsum"}
        cls.task = mommy.make(TaskReport)
        cls.task.result = cls.data
        cls.task.save()

    def test_list(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("tasks-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["uuid"])
        self.assertEqual(response.data[0]["result"], self.data)


class PerformanceTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.data = {"content": "lorem ipsum"}
        cls.p = mommy.make(Performance)

    def test_list(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse("performance-list")
        response = self.client.get(url, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]["start"])
        self.assertIsNotNone(response.data[0]["end"])
        self.assertIsNotNone(response.data[0]["event"])
        self.assertIsNotNone(response.data[0]["artist"])
