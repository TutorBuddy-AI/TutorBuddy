# required format of AI's answer
answer_schema = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "mistakes": {"type": ["array", "null"]},
    },
}
