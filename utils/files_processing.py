from typing import List, Tuple
from llama_index.core import  Document
from typing import List
import os
import llama_index
import pandas as pd
import json
from datetime import datetime
#import gspread
# from gspread_dataframe import get_as_dataframe
# from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from collections import Counter, defaultdict
# from pypdf import PdfReader
# from docx import Document
import regex as re
from oakdrf.logging_config import get_logger

logger = get_logger(__name__)

def custom_serializer(obj):
    """
    Serialize non-JSON serializable objects, such as datetime.
    Args:
        obj (any): The object to serialize.
    Returns:
        str: An ISO 8601 formatted string if the object is a datetime instance.
    Raises:
        TypeError: If the object type is not supported for serialization.
    """
    if isinstance(obj, datetime):
      return obj.isoformat()
    raise TypeError(f"Type {type(obj)} is not serializable")


def save_dict_to_json(input_dict: dict, file_path: str):
  '''
  This function saves the dictionary to JSON file
  Args:
    input dictionary, file path
  Returns:
    None
  '''
  with open(file_path, "w") as f:
    json.dump(input_dict, f, default=custom_serializer)

def load_dict_from_json(file_path: str) -> dict:
  '''
  This function loads the dictionary from json file
  Args:
    file path
  Returns:
    dictionary
  '''
  with open(file_path, "r") as f:
    loaded_dict  = json.load(f)
  return loaded_dict