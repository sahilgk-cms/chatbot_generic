import os
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.llms.google_genai import GoogleGenAI

load_dotenv()


OPENAI_API_KEY_1 = os.getenv("OPENAI_API_KEY_1")
OPENAI_API_KEYS = [OPENAI_API_KEY_1]

GOOGLE_API_KEY_1 = os.getenv("GOOGLE_API_KEY_1")
GOOGLE_API_KEY_2 = os.getenv("GOOGLE_API_KEY_2")
GOOGLE_API_KEYS = [GOOGLE_API_KEY_1, GOOGLE_API_KEY_2]

OPENAI_MODEL_NAME = "gpt-4o-mini"
GEMINI_MODEL_NAME = "models/gemini-2.0-flash"

LLM_CONFIG = {
    "Gemini": {
        "model": GEMINI_MODEL_NAME,
        "api_keys": GOOGLE_API_KEYS,
        "client_class": GoogleGenAI
    },
    "OpenAI": {
        "model": OPENAI_MODEL_NAME,
        "api_keys": OPENAI_API_KEYS,
        "client_class": OpenAI
    }
}

LOGS_DIRECTORY = os.path.join(os.getcwd(), "logs")

#print(GOOGLE_API_KEYS)

current_file_path = os.getcwd()

CHAT_PROMPT_TEMPLATE = (
      "The following text consists of some context, a question, and some instructions. "
      "Use the context to answer the question and follow the instructions while doing so."
      "\n\n----------- Start of Context ----------\n"
      "{text}\n"
      "\n----------- End of Context -----------\n"

       "\n\n----------- Start of Previous Conversation ----------\n"
    "You will also be provided with the history of previous messages between the user and the assistant. "
    "Use this history to maintain coherence, avoid repetition, and build upon prior discussion where relevant.\n"
    "Note: If the current query depends on something mentioned earlier, be sure to incorporate it.\n"
    "----------- End of Previous Conversation -----------\n"


      "When answering, please provide relevant supporting details and cite the specific part of the context where the answer is derived from."
   "Try to rephrase or summarize the relevant supporting details in your answer instead of using the exact same wording as present in the context."
   "Make sure your answer responds to the query being asked and does not contain irrelevant information or spelling mistakes."
   "Your answer should be concise and to the point while including all necessary details."
   "Try not to use too many bullet points with short sentences, only use them when necessary. You can use bullet points to list out important points or key details."
   "Your entire answer should not be longer than 500 words."
      "Please provide your response in **JSON format** with the following fields:\n"
      "```json\n"
      "{\n"
      '  "answer": "<Your concise answer here>",\n'
      '  "source": "<Plain text reference to where the answer is found>"\n'
      "}\n"
      "```\n"
      "If the answer is not found in the provided context, return:\n"
      "```json\n"
      '{ "answer": "Answer not found from the given context provided.", "source": "" }\n'
      "```\n"
      "\n----------- End of Instructions -----------\n"
   )



CASE_STORY_PROMPT_TEMPLATE = (
    "You are a development impact writer. Based on the context below, generate a NEW case story. "
    "Use a compelling, human-centered tone. Structure it with:\n"
    '''
    1. Title (Should capture the transformation)

    2. Context (2-3 lines)
    Geographic + thematic background
    Why this story matters

    3. The Problem
    What issue was being faced?
    Who was most affected?

    4. The Intervention
    What did the partner do?
    Who was involved (community, gov, other actors)?
    Mention any tools, processes (like participatory planning, legal training, MIS systems, etc.)

    5. Voices from the Ground (Optional)
    A quote or story from a beneficiary or frontline worker (Only if there is a quote in the provided context. If not, skip this.)

    6. Outcomes / Change Observed
    Tangible results — behavioural change, system-level changes, impact numbers if any

    7. What’s Next / Sustainability
    Is the change embedded?
    What are the next steps or replication ideas?
    '''

    "DO NOT copy any part of the example used earlier. Only use facts and ideas from the context.\n\n"
    "----------- CONTEXT -----------\n"
    "{context_str}\n"
    "----------- END CONTEXT -----------\n\n"
    "Start your case story below:"
)

CASE_STORY_ACROSS_ALL_ACTORS_TEMPLATE = (
    "You are a development impact writer. "
    "Using only the information provided in the context below, craft a comprehensive case story that captures key outcomes, changes, and impact across all social actors. "
    "Do not include any assumptions or fabricated details."
     "----------- CONTEXT -----------\n"
    "{context_str}\n"
    "----------- END CONTEXT -----------\n\n"
)





