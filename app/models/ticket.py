from jira import JIRA, Issue
from models import auth
from configs import config
from jinja2 import Environment, FileSystemLoader
import json
from services import base


class Ticket(Issue):
    def __init__(self, ticket_key):
        self.jira_auth = JIRA(server = config.server, basic_auth = config.basic_auth)
        super().__init__(self.jira_auth._options, self.jira_auth._session)
        self.find(ticket_key)
        config.logger.info(f'Ticket\'s {self.key} data was got')


    summary = lambda self: base.try_or(self.fields.summary.strip())
    type = lambda self: base.try_or(self.fields.issuetype.name)
    status = lambda self: base.try_or(self.fields.customfield_11803.currentStatus.status)
    priority = lambda self: base.try_or(self.fields.customfield_12302.value)
    description = lambda self: base.try_or(self.fields.description)
    last_comment = lambda self: base.try_or(self.fields.comment.comments[-1].body)
    customer_name = lambda self: base.try_or(self.fields.customfield_12101[0].name)
    creator_email = lambda self: base.try_or(self.fields.creator.emailAddress)
    reporter_email = lambda self: base.try_or(self.fields.comment.comments[-1].author.emailAddress)
    assignee_email = lambda self: base.try_or(self.fields.assignee.emailAddress)
    assignee_name = lambda self: base.try_or(self.fields.assignee.displayName)
    updating_time = lambda self: base.convert_date_in_utc(self.fields.customfield_11803.currentStatus.statusDate.iso8601)


    def assign(self, engineer_email_key):
        if not self.fields.assignee:
            self.jira_auth.assign_issue(self, config.team[engineer_email_key])
            self.jira_auth.add_watcher(self, config.team[engineer_email_key])
            config.logger.info('Ticket was assigned')


    def first_response(self):
        if self.type() == "Incident":
            comments =  self.fields.comment.comments
            for comment in comments:
                if comment.author.displayName == 'Technical support AP':
                    return
            if self.priority() == 'High':
                first_response = "Здравствуйте! \nВаш запрос обрабатывается. \nПожалуйста, ожидайте обновления заявки в течение 4 часов или ранее."
            elif self.priority() == 'Medium':
                first_response = "Здравствуйте! \nВаш запрос обрабатывается. \nПожалуйста, ожидайте обновления заявки в течение 8 часов или ранее."
            elif self.priority() == 'Low':
                first_response = "Здравствуйте! \nВаш запрос обрабатывается. \nПожалуйста, ожидайте обновления заявки в течение 16 часов или ранее."
            self.jira_auth.add_comment(self, first_response)
            self.jira_auth.remove_watcher(self, config.basic_auth[0])
            config.logger.info('Ticket was responsed')


    def get_teams_card_created(self):
        environment = Environment(loader=FileSystemLoader("templates/tickets/"))
        template = environment.get_template("created.j2")
        self.api_token = auth.generate_api_token()
        rendered_template = template.render(ticket=self, team=config.team)
        teams_card = json.loads(rendered_template, strict=False)

        config.logger.info('Message card for Teams was created')
        config.logger.info(str(teams_card))
        return teams_card


    def get_teams_card_updated(self):
        environment = Environment(loader=FileSystemLoader("templates/tickets/"))
        template = environment.get_template("updated.j2")
        rendered_template = template.render(ticket=self, team=config.team)
        teams_card = json.loads(rendered_template, strict=False)

        config.logger.info('Message card for Teams was created')
        config.logger.info(str(teams_card))
        return teams_card

