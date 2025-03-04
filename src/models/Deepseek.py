from openai import OpenAI
from .Model import Model


class Deepseek(Model):
    def __init__(self, config):
        super().__init__(config)
        api_keys = config["api_key_info"]["api_keys"]
        api_pos = int(config["api_key_info"]["api_key_use"])
        assert (0 <= api_pos < len(api_keys)), "Please enter a valid API key to use"
        self.max_output_tokens = int(config["params"]["max_output_tokens"])
        self.api_key = api_keys[api_pos]
        #self.client = OpenAI(api_key=api_keys[api_pos], base_url="https://api.deepseek.com")

    def query(self, msg):

        client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
        try:
            #print(f"model: {self.name}\n")
            #print(f"temperature: {self.temperature}\n")
            #print(f"max_tokens: {self.max_output_tokens}\n")

            #print(f"prompt: {msg} \n ****** \n")
            completion = ""
            i = 0
            while completion == "" and i<10:
                completion = client.chat.completions.create(
                    model=self.name,
                    temperature=self.temperature,  # temperature is not used in deepseek-reasoner
                    max_tokens=self.max_output_tokens,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": msg}
                    ],
                )   
                i += 1
            if i>=3:
                print(f"3 times no response\n")
            response = completion.choices[0].message.content
           
        except Exception as e:
            print(f"Exception: {e}\n")
            response = ""

        return response