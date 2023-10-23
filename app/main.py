from  fastapi import FastAPI, responses, Depends
import requests
from configs import config
from models import ticket, auth

app = FastAPI()


@app.get('/')
async def index(api_token):
    auth.api_token_auth(api_token)
    return {'message': 'We are working to solve this. May the force be with you!'}


@app.get('/health')
async def check_health():
    return {"status":"ok"}


@app.get('/ticket_assign')
async def get_model(ticket_key, engineer_key, api_token):
    auth.api_token_auth(api_token)
    config.logger.info('Ticket assignee: Request was received')

    issue = ticket.Ticket(ticket_key)
    issue.assign(engineer_key)
    issue.first_response()

    return responses.RedirectResponse(f"https://jira.activeplatform.com/browse/{ticket_key}")


@app.post('/ticket_updated', dependencies=[Depends(auth.api_token_auth)])
async def process_updated_ticket(request: dict):
    config.logger.info('Ticket updated: Request was received')
    
    issue = ticket.Ticket(request['issue']['key'])   
    teams_card = issue.get_teams_card_updated()
    request = requests.post(config.WEBHOOK_URL, json=teams_card)

    config.logger.info(str(teams_card))
    return {'message': 'Data was processed!'}


@app.post('/ticket_created', dependencies=[Depends(auth.api_token_auth)])
async def process_created_ticket(request: dict):
    config.logger.info('Ticket created: Request was received')

    issue = ticket.Ticket(request['issue']['key']) 
    teams_card = issue.get_teams_card_created()
    request = requests.post(config.WEBHOOK_URL, json=teams_card)

    config.logger.info((str(teams_card)))
    return {'message': 'Data was processed!'}



