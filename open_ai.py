from openai import OpenAI

# 1. Replace this with the URL you copied from Step 2
# MUST include "/v1" at the end of the URL!
class OPENAI : 
    def __init__(self):
        self.CLOUDFLARE_URL = "https://hose-medal-designated-partnerships.trycloudflare.com/v1"
    
    def infer(self,input):
        print(f"Connecting to: {self.CLOUDFLARE_URL}")

        # 2. Initialize the OpenAI client pointing to your server
        client = OpenAI(
            api_key="sk-dummy-key", # vLLM doesn't check this by default, but the SDK requires a string
            base_url=self.CLOUDFLARE_URL,
        )

        # 3. Send a ChatCompletion request
        response = client.chat.completions.create(
            model="saudi-dialect", # This matches the --served-model-name we set earlier
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ومفيد تتحدث باللهجة السعودية."},
                {"role": "user", "content": input}
            ],
            temperature=0.7,
            max_tokens=256
        )
        
        # Extract and print the message content
        message_content = response.choices[0].message.content
        print(f"Message content: {message_content}")
        
        return response,message_content
if __name__ == 'main':
    pass 