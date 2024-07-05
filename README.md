### Setting
import setting to set the LLM model


```python

from llama_index.core import Settings

# import the LLM model
from llama_index.llms.openai import OpenAI


# define global LLM
Settings.llm = OpenAI(temperature=0, model="gpt-3.5-turbo", max_tokens=512)

```


### Using Vector Stores
