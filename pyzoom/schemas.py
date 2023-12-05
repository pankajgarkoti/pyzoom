from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel
from typing_extensions import Literal


class MyZoomBase(BaseModel):
    class Config:
        from_attributes = True

    def pprint(self):
        from pprint import pprint

        pprint(self.dict())


class ZoomMeetingSettings(MyZoomBase):
    host_video: bool
    participant_video: bool
    cn_meeting: bool
    in_meeting: bool
    join_before_host: bool
    mute_upon_entry: bool
    watermark: bool
    use_pmi: bool
    approval_type: Literal[0, 1, 2] = 2
    registration_type: Optional[Literal[1, 2, 3]] = 2
    audio: Literal["voip", "telephony", "both"]
    auto_recording: Literal["local", "cloud", "none"]
    enforce_login: bool
    enforce_login_domains: Optional[str] = None
    alternative_hosts: Optional[str] = None
    close_registration: Optional[bool] = None
    waiting_room: bool
    global_dial_in_countries: Optional[List[str]] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    registrants_email_notification: bool
    meeting_authentication: bool
    authentication_option: Optional[str] = None
    authentication_domains: Optional[str] = None
    meeting_invitees: Optional[list[dict]] = None

    @classmethod
    def default_settings(cls) -> ZoomMeetingSettings:
        return ZoomMeetingSettings(
            host_video=True,
            participant_video=True,
            join_before_host=True,
            mute_upon_entry=True,
            approval_type=0,
            cn_meeting=False,
            in_meeting=False,
            watermark=False,
            use_pmi=False,
            registration_type=2,
            audio="telephony",
            auto_recording="none",
            enforce_login=False,
            waiting_room=True,
            registrants_email_notification=True,
            meeting_authentication=False,
            contact_name="UFY",
            contact_email="ufyit@support.com",
        )


class ZoomMeetingShort(MyZoomBase):
    uuid: str
    id: int
    host_id: str
    topic: str
    type: int
    start_time: Optional[str] = None
    duration: int
    timezone: str
    created_at: str
    join_url: str


class ZoomMeeting(ZoomMeetingShort):
    status: str
    agenda: Optional[str] = None
    start_url: str
    registration_url: Optional[str] = None
    password: str
    h323_password: str
    pstn_password: str
    encrypted_password: str
    settings: ZoomMeetingSettings


class ZoomMeetingShortList(MyZoomBase):
    page_count: Optional[int] = None
    page_number: Optional[int] = None
    page_size: int
    total_records: int
    meetings: List[ZoomMeetingShort]
    next_page_token: Optional[str] = None

    def filter_by_topic(self, text: str) -> List[ZoomMeetingShort]:
        return [m for m in self.meetings if text.lower() in m.topic.lower()]

    def filter_by_id(self, meeting_id: int) -> List[ZoomMeetingShort]:
        return [m for m in self.meetings if m.id == meeting_id]


class MeetingRegistrantShort(MyZoomBase):
    id: Optional[str] = None
    email: Optional[str] = None


class MeetingRegistrant(MeetingRegistrantShort):
    email: str
    first_name: str
    last_name: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    industry: Optional[str] = None
    org: Optional[str] = None
    job_title: Optional[str] = None
    comment: Optional[str] = None


class MeetingRegistrantsList(MyZoomBase):
    page_count: int
    page_number: int
    page_size: int
    total_records: int
    registrants: List[MeetingRegistrant]


class RegistrantConfirmation(MyZoomBase):
    registrant_id: str
    id: int
    topic: str
    start_time: str
    join_url: str


class MeetingParticipant(MyZoomBase):
    id: str
    name: str
    user_email: str


class MeetingParticipantList(MyZoomBase):
    page_count: int
    page_size: int
    total_records: int
    participants: Optional[List[MeetingParticipant]] = []

    def __len__(self):
        return len(self.participants)

    def __iter__(self):
        return iter(self.participants)

    def __getitem__(self, index):
        return self.participants[index]

    def find_by_id(self, id_: str) -> List[MeetingParticipant]:
        return [i for i in self.participants if i.id == id_]

    def find_by_email(self, email: str) -> List[MeetingParticipant]:
        return [i for i in self.participants if i.user_email == email]

    def find_by_name(self, name):
        return [i for i in self.participants if i.name == name]


class ZoomUser(MyZoomBase):
    id: str
    first_name: str
    last_name: str
    email: str
    type: int
    pmi: int
    timezone: Optional[str] = None
    verified: int
    dept: Optional[str] = None
    created_at: str
    pic_url: Optional[str] = None
    group_ids: Optional[List[str]]
    language: Optional[str] = None
    phone_number: Optional[str] = None
    status: str
    role_id: str


class ZoomUserList(MyZoomBase):
    page_count: int
    page_number: int
    page_size: int
    total_records: int
    users: List[ZoomUser]
