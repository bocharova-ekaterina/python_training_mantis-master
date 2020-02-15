from suds.client import Client
from suds import WebFault
from model.project import Project
import json

class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        wd = self.app.wd
        client = Client(self.app.base_url + "/api/soap/mantisconnect.php" + "?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list(self, username, password):
        client = Client(self.app.base_url + "/api/soap/mantisconnect.php" + "?wsdl")
        try:
            list =[]
            res=client.service.mc_projects_get_user_accessible(username, password)
            for projects in res:
                project = Project(id=projects.id, name=str(projects.name), status=projects.view_state,
                                  inherit_global=projects.enabled, description=projects.description)
            return list.append(project)
        except WebFault:
            return ('SOAP Error')