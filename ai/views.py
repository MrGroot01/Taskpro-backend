import json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings


class AISuggestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title', '').strip()
        if not title:
            return Response({'error': 'Title is required.'}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"""You are a professional project manager. Given the rough task title "{title}", generate:
1. A clear, professional task title
2. A detailed description (2-3 sentences)
3. A priority level (must be exactly: low, medium, or high)

Respond ONLY with JSON, no markdown, no explanation:
{{"title": "...", "description": "...", "priority": "..."}}"""

        # Try Groq first (faster, generous free tier)
        groq_key = getattr(settings, 'GROQ_API_KEY', '')
        if groq_key:
            result = self._try_groq(prompt, groq_key)
            if result:
                return Response(result)

        # Fallback to Gemini
        gemini_key = getattr(settings, 'GEMINI_API_KEY', '')
        if gemini_key:
            result = self._try_gemini(prompt, gemini_key)
            if result:
                return Response(result)

        return Response(
            {'error': 'AI service unavailable. Fill in description manually.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    def _try_groq(self, prompt, api_key):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 300,
            }
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            raw_text = data['choices'][0]['message']['content']
            raw_text = raw_text.strip().strip('```json').strip('```').strip()
            result = json.loads(raw_text)
            return self._clean_result(result)
        except Exception:
            return None

    def _try_gemini(self, prompt, api_key):
        models = ['gemini-2.0-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
        for model in models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 300}
                }
                response = requests.post(url, json=payload, timeout=15)
                if response.status_code in [404, 429]:
                    continue
                response.raise_for_status()
                data = response.json()
                raw_text = data['candidates'][0]['content']['parts'][0]['text']
                raw_text = raw_text.strip().strip('```json').strip('```').strip()
                result = json.loads(raw_text)
                return self._clean_result(result)
            except Exception:
                continue
        return None

    def _clean_result(self, result):
        priority = result.get('priority', 'medium').lower()
        if priority not in ['low', 'medium', 'high']:
            priority = 'medium'
        return {
            'title': result.get('title', ''),
            'description': result.get('description', ''),
            'priority': priority,
        }