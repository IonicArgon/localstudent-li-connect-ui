# imports up here
from app.base import Base
import pprint
# type import
from requests.models import Response
import requests


# exceptions
class LinkedInMemberObjDoesNotExist(Exception):
    pass

class LinkedInMemberObjMalformed(Exception):
    pass

class LinkedInProfileObjMalformed(Exception):
    pass

class LeadsConnector(Base):
    def __init__(self, headers: str = None, cookies: str = None):
        super().__init__(headers=headers, cookies=cookies)

    def get_profile(self, profile_id: str) -> dict:
        params = {
            "q": "memberIdentity",
            "memberIdentity": profile_id,
            "decorationId": "com.linkedin.voyager.dash.deco.identity.profile.WebTopCardCore-16",
        }

        self.m_session.headers.update({"User-Agent": self.get_user_agent()})

        response = self.m_session.get(
            "https://www.linkedin.com/voyager/api/identity/dash/profiles",
            params=params,
            timeout=10,
            allow_redirects=False
        )
        redirect_link = None

        # check if the profile was redirected
        if response.status_code == 302:
            redirect_link = response.headers["Location"]

            # attempt to follow the redirect
            response = self.m_session.get(
                redirect_link,
                timeout=10,
                allow_redirects=False
            )

            # if it's still a redirect, we'll print out info and return None
            if response.status_code == 302:
                print(f"Error with profile {profile_id}! Redirected to {redirect_link} and then to {response.headers['Location']}. Dumping informaton:\n")
                print("Headers:")
                pprint.pprint(response.headers)
                print("\nBody:")
                pprint.pprint(response.text)
                return None
        
        if response.status_code != 200:
            return None
        
        return response.json()
    
    def get_profile_urn(self, json_data: dict) -> str:
        elements_first = json_data.get("data", None)

        if elements_first is None:
            raise LinkedInProfileObjMalformed(
                "LinkedIn profile object is malformed! Maybe LinkedIn changed their API?"
            )
        
        # look for a value starting with "urn:li:fsd_profile:" within the json
        urn = None
        urn = elements_first["*elements"][0]

        if urn is None:
            raise LinkedInProfileObjMalformed(
                "LinkedIn profile object is malformed! Maybe LinkedIn changed their API?"
            )
        
        return urn
    
    def connect_to_profile(self, profile_urn, message: str = "") -> Response:
        params = {
            "action": "verifyQuotaAndCreateV2",
            "decorationId": "com.linkedin.voyager.dash.deco.relationships.InvitationCreationResultWithInvitee-2"
        }

        payload = {
            "invitee": {
                "inviteeUnion": {
                    "memberProfile": profile_urn
                }
            },
            "customMessage": message,
        }

        self.m_session.headers.update({"User-Agent": self.get_user_agent()})

        print(f"attempting to connect to {profile_urn} with message {message}")

        response = self.m_session.post(
            "https://www.linkedin.com/voyager/api/voyagerRelationshipsDashMemberRelationships",
            params=params,
            json=payload,
            timeout=10
        )

        #! if it fails with a 400 with the code "CANT_RESEND_YET" then we'll need to wait like 3 weeks
        #todo: add a check for this
        
        return response

