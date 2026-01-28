from anthropic import AsyncAnthropic

class Stage:
    """Evaluate items against a criteria using Claude. Returns YES/NO"""
    
    def __init__(
        self,
        name: str, # e.g. Stage1
        criteria: str, # for best results include Role, Instruction, <examples_YES>, <examples_NO>,
        model: str = "claude-3-haiku-20240307", # change per stage. Later stages should be smarter, use more reasoning
        max_tokens: int = 1000, # or you could just ignore this
    ):
        self.client = AsyncAnthropic()
        self.name = name
        self.criteria = criteria
        self.model = model
        self.max_tokens = max_tokens

  
    async def run(self, text: str) -> bool:
        system = f"Evaluate if this text meets the criteria: {self.criteria}\n\nRespond with only YES or NO." 
        
        response = await self.client.messages.create(
            model=self.model,
            system=system,
            messages=[{"role": "user", "content": text}],
            max_tokens=self.max_tokens,
        )
        
        answer = response.content[0].text.strip().lower() # lower to remove case sensitivity
        return "yes" in answer and "no" not in answer # Boolean True/False. Any confused replies including both "YES" and "NO" become False. 
