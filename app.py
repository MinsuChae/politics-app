from flask import Flask
from dotenv import load_dotenv
import os
from route.party_detail import party_detail
from route.candidate_detail import candidate_detail
from route.ask_candidate import ask_candidate, ask_all_candidates
from route.index import index
from data.data_loader import reload_data

load_dotenv()
reload_data()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
app = Flask(__name__)
app.secret_key = SECRET_KEY

app.add_url_rule('/', view_func=index)
app.add_url_rule('/party/<party_slug>', endpoint='party_detail', view_func=party_detail)
app.add_url_rule('/party/<party_slug>/candidate/<int:candidate_index>', endpoint='candidate_detail', view_func=candidate_detail)
app.add_url_rule('/party/<party_slug>/candidate/<int:candidate_index>/ask', view_func=ask_candidate, methods=['POST'])
app.add_url_rule('/ask/all', view_func=ask_all_candidates, methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)