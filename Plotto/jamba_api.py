import os
from ai21 import AI21Client
from ai21.models.chat import ChatMessage, ResponseFormat, DocumentSchema, FunctionToolDefinition, ToolDefinition, ToolParameters

secret_key = 'Qk7khbnHvbdBx7Du4TMCi2EqQQqic7sO'

client = AI21Client(api_key=secret_key)
response = client.chat.completions.create(
    model="jamba-1.5-large",
    messages= [ {"role": "user", "content": "What is the capital of France?"} ],
    documents=[],
    tools=[],
    n=1,
    max_tokens=2048,
    temperature=0.4,
    top_p=1,
    stop=[],
    response_format=ResponseFormat(type="text"),
)

# Print the response
print(response.choices[0].message.content)
