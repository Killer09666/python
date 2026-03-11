import os
import re
import random
from datetime import datetime

# Optional: Uncomment if you have OpenAI API key
# from openai import OpenAI

class HybridChatbot:
    def __init__(self, api_key=None):
        """Initialize with both rule-based and AI capabilities."""
        
        # Initialize OpenAI client if API key is available
        self.use_ai = False
        if api_key or os.getenv('OPENAI_API_KEY'):
            try:
                if api_key is None:
                    api_key = os.getenv('OPENAI_API_KEY')
                # Uncomment these lines when you have an API key
                # self.client = OpenAI(api_key=api_key)
                # self.use_ai = True
                # self.conversation_history = [
                #     {"role": "system", "content": "You are a helpful, friendly AI assistant."}
                # ]
            except:
                self.use_ai = False
        
        self.user_name = "Friend"
        self.name = "ChatBot"
        
        # Rule-based responses for quick queries
        self.quick_responses = {
            'time': lambda: f"The current time is {datetime.now().strftime('%I:%M %p')}.",
            'date': lambda: f"Today's date is {datetime.now().strftime('%B %d, %Y')}.",
            'weather': lambda: "I don't have real-time weather data, but I'd recommend checking your favorite weather app!",
            'help': lambda: "I can help with many things! Try asking me about: time, date, general questions, or just have a conversation!",
            'joke': lambda: "Why did the AI go to therapy? Because it had too many deep learning issues! 😄",
            'quote': lambda: "Here's a thought: 'The only way to do great work is to love what you do.' - Steve Jobs",
        }
    
    def get_ai_response(self, user_input):
        """Get response from OpenAI API."""
        if not self.use_ai:
            return None
        
        try:
            self.conversation_history.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                max_tokens=150,
                temperature=0.7
            )
            
            bot_response = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            
            return bot_response
        except:
            return None
    
    def get_rule_based_response(self, user_input):
        """Handle common queries with rule-based responses."""
        user_input_lower = user_input.lower().strip()
        
        # Check for quick response triggers
        for key, response_func in self.quick_responses.items():
            if key in user_input_lower:
                return response_func()
        
        # Check for name-related queries
        if any(word in user_input_lower for word in ["your name", "who are you", "what are you"]):
            return f"I'm {self.name}, your AI assistant! I'm here to help and chat with you."
        
        if "my name" in user_input_lower:
            name_match = re.search(r"my name is (\w+)", user_input_lower)
            if name_match:
                self.user_name = name_match.group(1)
                return f"Nice to meet you, {self.user_name}! I'll remember that."
            return f"Your name is {self.user_name}, right? That's a great name!"
        
        # Check for greetings
        greeting_patterns = [r'\b(hi|hello|hey|howdy)\b']
        if any(re.search(pattern, user_input_lower) for pattern in greeting_patterns):
            responses = [
                f"Hello {self.user_name}! How are you doing today?",
                f"Hi there, {self.user_name}! What's on your mind?",
                f"Hey {self.user_name}! Great to see you!"
            ]
            return random.choice(responses)
        
        # Check for feelings
        positive_words = ['happy', 'great', 'awesome', 'excellent', 'good', 'wonderful', 'joy']
        negative_words = ['sad', 'unhappy', 'upset', 'bad', 'terrible', 'angry', 'depressed']
        
        if any(word in user_input_lower for word in positive_words):
            responses = [
                f"That's wonderful to hear, {self.user_name}! What's making you feel so good?",
                "I love that positive energy! Keep it up!",
                "That's fantastic! I'd love to hear more about what's bringing you joy!"
            ]
            return random.choice(responses)
        
        if any(word in user_input_lower for word in negative_words):
            responses = [
                f"I'm sorry you're feeling this way, {self.user_name}. Do you want to talk about it?",
                "Remember, it's okay to not feel okay sometimes. I'm here to listen.",
                "I'm sorry to hear that. Would you like to share what's troubling you?"
            ]
            return random.choice(responses)
        
        # Check for thanks
        if any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate']):
            responses = [
                "You're very welcome! Happy to help!",
                "Anytime! That's what I'm here for!",
                "My pleasure! Don't hesitate to ask if you need anything else."
            ]
            return random.choice(responses)
        
        # Check for how are you
        if 'how are you' in user_input_lower:
            return "I'm doing great, thank you for asking! How can I help you today?"
        
        # Check for exit
        if any(word in user_input_lower for word in ['bye', 'goodbye', 'quit', 'exit', 'stop']):
            return "EXIT"
        
        # No rule matched
        return None
    
    def get_response(self, user_input):
        """Get response using rule-based first, then AI if available."""
        
        # Try rule-based first
        rule_response = self.get_rule_based_response(user_input)
        
        if rule_response == "EXIT":
            return None, True  # Signal to exit
        
        if rule_response:
            return rule_response, False
        
        # If no rule matched and AI is available, use AI
        if self.use_ai:
            ai_response = self.get_ai_response(user_input)
            if ai_response:
                return ai_response, False
        
        # Default responses when nothing matches
        default_responses = [
            "That's interesting! Tell me more about that.",
            "I see. Could you elaborate a bit more?",
            "That's a fascinating perspective! What else is on your mind?",
            "I'd love to hear more about that!",
            "Interesting! What do you think about that?"
        ]
        return random.choice(default_responses), False
    
    def run(self):
        """Main conversation loop."""
        print("\n" + "="*50)
        print("🤖 Welcome to Your AI Chatbot!")
        print("="*50)
        print("Type 'quit', 'exit', or 'bye' to end our conversation.\n")
        
        if self.use_ai:
            print("✨ AI Mode: ENABLED (Powered by OpenAI)")
        else:
            print("📝 Mode: Rule-Based Chatbot")
        
        print("-"*50 + "\n")
        
        self.user_name = input("What's your name? ").strip()
        if not self.user_name:
            self.user_name = "Friend"
        
        print(f"\n✨ Nice to meet you, {self.user_name}! Let's chat!\n")
        
        while True:
            try:
                user_input = input(f"{self.user_name}: ").strip()
                
                if not user_input:
                    print("Bot: Please say something! I'm here to chat.\n")
                    continue
                
                # Get response
                response, should_exit = self.get_response(user_input)
                
                if should_exit:
                    print(f"\n🤖 Bot: Goodbye {self.user_name}! It was wonderful chatting with you!")
                    print("Bot: Take care and don't hesitate to come back! 👋\n")
                    break
                
                print(f"Bot: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n🤖 Bot: Goodbye {self.user_name}! Take care! 👋\n")
                break

# Run the chatbot
if __name__ == "__main__":
    chatbot = HybridChatbot()
    chatbot.run()