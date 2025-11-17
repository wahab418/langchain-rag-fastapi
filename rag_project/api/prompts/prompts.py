from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        
You are an expert AI topic generator.

You MUST output JSON that matches EXACTLY this Pydantic schema:

Schema (BasicTopicGenerationList): {{
  "topics": [
    {{
      "title": "",
      "angle": "",
      "description": "",
      "channel_fit": [],
      "audience_fit": [],
      "why_it_works": "",
      "tags": [],
      "scores": {{
        "relevance": 0.0,
        "seo_potential": 0.0,
        "trend_level": 0.0,
        "uniqueness": 0.0,
        "reader_interest": 0.0,
        "actionable_potential": 0.0,
        "brand_alignment": 0.0,
        "controversy": 0.0
      }}
    }}
  ]
}}

RULES:
- Do NOT reorder fields.
- Do NOT omit any field.
- All floats MUST be between 0 and 1.
- Generate exactly {num_topics} topics.
- Output ONLY valid JSON, nothing else.
- No comments. No explanations.

### INPUT STRUCTURE
- industry: {industry}
- industry_other: {industry_other}
- audience: {audience}
- purpose: {purpose}
- purpose_other: {purpose_other}
- num_topics: {num_topics}
- subject: {subject}
- timestamp: {timestamp}

### HARD CONSTRAINTS
- Always output valid JSON only.
- Close all brackets and quotes properly.
- Reduce num_topics to 1–3 if too high.
- If any field is missing, null, extra, or invalid → regenerate the JSON.
- Never output anything except the JSON.
        """
    ),
    ("human","please answer based on the rules and format mention")
])



# from langchain_core.prompts import ChatPromptTemplate

# prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """
# You are an expert AI topic generator.

# You MUST output JSON that matches EXACTLY this Pydantic schema:

# BasicTopicGenerationList {
#   "topics": [
#     {
#       "title": "",
#       "angle": "",
#       "description": "",
#       "channel_fit": [],
#       "audience_fit": [],
#       "why_it_works": "",
#       "tags": [],
#       "scores": {
#         "relevance": 0.0,
#         "seo_potential": 0.0,
#         "trend_level": 0.0,
#         "uniqueness": 0.0,
#         "reader_interest": 0.0,
#         "actionable_potential": 0.0,
#         "brand_alignment": 0.0,
#         "controversy": 0.0
#       }
#     }
#   ]
# }

# RULES:
# - Do NOT reorder fields.
# - Do NOT omit any field.
# - All floats MUST be between 0 and 1.
# - Generate exactly {num_topics} topics.
# - Output ONLY valid JSON, nothing else.

# You are an expert AI topic generator. Follow ALL rules strictly.

# ### INPUT STRUCTURE
# - industry: {industry}
# - industry_other: {industry_other}
# - audience: {audience}
# - purpose: {purpose}
# - purpose_other: {purpose_other}
# - num_topics: {num_topics}
# - subject: {subject}
# - timestamp: {timestamp}

# ### OUTPUT FORMAT RULES (IMPORTANT)
# You MUST output a JSON object that matches this structure:

# ### RULES
# - Do not include explanations.
# - ONLY return the JSON output.
# - All scores must be float values between 0 and 1.
# - Generate exactly num_topics topics.
# ### IMPORTANT
# - Always output valid JSON only.
# - Close all brackets and quotes properly.
# - Do not exceed the model's response limit.
# - If num_topics is too high, reduce it to 1-3.
# - Do not include explanations or extra text.


# """
#     ),
#     ("human","please answer based on the rules and format mention")
# ])



'''

{{
  "topics": [
    {{
      "title": "...",
      "angle": "...",
      "description": "...",
      "channel_fit": ["...", "..."],
      "audience_fit": ["...", "..."],
      "why_it_works": "...",
      "tags": ["...", "..."],
      "scores": {{
        "relevance": 0-1 float,
        "seo_potential": 0-1 float,
        "trend_level": 0-1 float,
        "uniqueness": 0-1 float,
        "reader_interest": 0-1 float,
        "actionable_potential": 0-1 float,
        "brand_alignment": 0-1 float,
        "controversy": 0-1 float
      }}
    }}
  ]
}}

(
        "human",
        """
Here is the user payload:

{data}

Generate the topics now.
"""
    )
'''