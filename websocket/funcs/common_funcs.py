from django.urls import reverse
from dotenv import load_dotenv
import os
import shutil
import json
import math
import time
import random
import string
import base64
import hashlib
from datetime import datetime
from urllib.parse import urlencode, urljoin
from pasapo_websocket.settings import (
    logger,
    apikeys_col,
    users_col,
    properties_col,
    rooms_col,
    guests_col,
    types_col,
    notifications_col, 
    contacts_col,
    links_col
)
import uuid
import io
from difflib import SequenceMatcher
from bson import ObjectId
