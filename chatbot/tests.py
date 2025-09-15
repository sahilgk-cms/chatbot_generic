from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from unittest.mock import patch
from chatbot.models import ChatSession, ChatMessage
import uuid


# Create your tests here.
class ChatbotAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/chatbot/chat/"

    @patch("chatbot.views.qa_chat_with_prompt")
    def test_start_new_chat(self, mock_qa):
        """
            Test: starting a new chat session (no session_id provided).
            - We mock qa_chat_with_prompt to avoid calling the real LLM.
            - Expect: API returns 200, creates a session, and saves 2 messages.
        """

        # Mock the return value of qa_chat_with_prompt
        mock_qa.return_value = {"answer": "This is a test answer", "source": "mocked"}

        # Send POST request to our API
        response = self.client.post(self.url,
                                    {
                                        "text": "phase 1",
                                        "query": "tell me something"
                                    },
                                    format="json")

        # Assertions = checks we expect to be true
        # API worked
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # New session created
        self.assertIn("session_id", response.data)

        # user + assistant saved
        self.assertEqual(ChatMessage.objects.count(), 2)

    @patch("chatbot.views.qa_chat_with_prompt")
    def test_continue_chat_existing_session(self, mock_qa):
        """
        Test: continue a chat using an existing session_id.
        - First we create a ChatSession manually.
        - Expect: API uses the same session, and saves 2 more messages.
        """

        mock_qa.return_value = {"answer": "Continue", "source": "mocked"}

        # Create a fake session in DB
        session = ChatSession.objects.create(id=str(uuid.uuid4()))

        # Send request with session_id
        response = self.client.post(self.url, {
            "session_id": str(session.id),
            "text": "phase 1",
            "query": "What next?"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Works
        self.assertEqual(response.data["session_id"], str(session.id))  # Reused old session
        self.assertEqual(ChatMessage.objects.filter(session=session).count(), 2)  # 2 messages added

    def test_invalid_serializer(self):
        """
        Test: sending invalid data (missing query).
        - Serializer should reject it.
        - Expect: 400 Bad Request with error details.
        """
        response = self.client.post(self.url,
                                    {
                                        "text": "phase 1"
                                    }, format = "json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("chatbot.views.qa_chat_with_prompt", side_effect = Exception("mocked failure"))
    def test_qa_chat_with_failure(self, mock_qa):
        """
        Test: simulate qa_chat_with_prompt crashing.
        - We force it to raise an Exception.
        - Expect: API returns 500 Internal Server Error.
        """
        response = self.client.post(self.url,
                                    {
                                        "text": "phase 1",
                                        "query": "fail please"
                                    }, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)

