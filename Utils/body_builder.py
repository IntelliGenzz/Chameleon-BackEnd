import json

async def body_builder(client, userInput: str, max_tokens: int = 1000):
    body = {
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': max_tokens,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': userInput
                    }
                ]
            },
        ]
    }
    
    response = await client.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        contentType='application/json',
        accept='application/json',
        body=json.dumps(body)
    )
    return response
