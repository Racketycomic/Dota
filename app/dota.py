from app import app,db
from app.models import logo,player,hero,player_hero,ana,match,player_match
@app.shell_context_processor

def make_shell_processor():
    return {'db':db,'logo':logo,'player':player,'player_hero':player_hero,'hero':hero,'ana':ana,'match':match,'player_match':player_match}
