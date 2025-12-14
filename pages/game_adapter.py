from flask import Blueprint, request
import json
from lib.general import ok, fail
import lib.model as LLMService
from game_core.game_core import LLMInterface, RAGInterface, GameClassifier
from game_core.game_factory import AgentFactory

app = Blueprint('game_adapter', __name__)

class FlaskLLMAdapter(LLMInterface):
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        return LLMService.ask_llm(text=user_prompt, system=system_prompt)

class FlaskRAGAdapter(RAGInterface):
    def retrieve_game_rules(self, game_name: str) -> str:
        try:
            from main import GLOBAL_RAG
            if GLOBAL_RAG:
                result = GLOBAL_RAG.answer_query(f"What are the rules and strategies for {game_name}?")
                return result.get('answer', 'No info found.')
            return "RAG Service unavailable."
        except ImportError:
            return "RAG Service unavailable."

@app.route('/game/play_turn', methods=['POST'])
def play_turn():
    try:
        rules = request.values.get('rules', '')
        user_move = request.values.get('move', '')
        history_raw = request.values.get('history', '[]')
        
        try:
            history = json.loads(history_raw)
        except:
            history = []

        llm_adapter = FlaskLLMAdapter()
        rag_adapter = FlaskRAGAdapter()

        classifier = GameClassifier(llm_adapter)
        classification = classifier.classify("Current Game", rules)
        
        if 'type' not in classification:
            return fail(f"Game Classification Failed: {classification}")
            
        game_type = classification['type']

        agent = AgentFactory.create_agent(
            agent_type_code=game_type, 
            agent_id="AI_Opponent", 
            config={}, 
            llm=llm_adapter, 
            rag=rag_adapter
        )

        agent.memory = history 

        game_state = {
            "rules": rules,
            "turn": len(history) + 1,
            "last_user": user_move
        }
        
        decision = agent.think_and_act(game_state)
        decision['debug_game_type'] = game_type
        
        return ok(decision)

    except Exception as e:
        return fail(f"Adapter Error: {str(e)}")