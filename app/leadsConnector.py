# imports up here
from app.base import Base
import pprint
# type import
from requests.models import Response


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
        )

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

