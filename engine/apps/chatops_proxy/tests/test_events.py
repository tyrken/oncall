from unittest.mock import patch

import pytest
from django.test import override_settings

from apps.chatops_proxy.events import ChatopsEventsHandler
from apps.chatops_proxy.events.handlers import SlackInstallationHandler
from common.constants.slack_auth import SLACK_OAUTH_ACCESS_RESPONSE

installation_event = {
    "event_type": "integration_installed",
    "data": {
        "provider_type": "slack",
        "stack_id": "stack_id",
        "grafana_user_id": "grafana_user_id",
        "payload": SLACK_OAUTH_ACCESS_RESPONSE,
    },
}

unknown_event = {
    "event_type": "unknown_event",
    "data": {
        "provider_type": "slack",
        "stack_id": "stack_id",
        "grafana_user_id": "grafana_user_id",
        "payload": {},
    },
}

invalid_schema_event = {
    "a": "b",
    "c": "d",
}


@patch.object(ChatopsEventsHandler, "_exec", return_value=None)
@pytest.mark.parametrize(
    "payload,is_handled",
    [
        (installation_event, True),
        (unknown_event, False),
        (invalid_schema_event, False),
    ],
)
@pytest.mark.django_db
@override_settings(UNIFIED_SLACK_APP_ENABLED=True)
def test_root_event_handler(mock_exec, payload, is_handled):
    h = ChatopsEventsHandler()
    assert h.handle(payload) is is_handled


@patch("apps.chatops_proxy.events.handlers.install_slack_integration", return_value=None)
@pytest.mark.django_db
def test_slack_installation_handler(mock_install_slack_integration, make_organization_and_user):
    organization, user = make_organization_and_user()

    installation_event["data"].update({"stack_id": organization.stack_id, "grafana_user_id": user.user_id})

    h = SlackInstallationHandler()

    assert h.match(unknown_event) is False
    assert h.match(invalid_schema_event) is False

    assert h.match(installation_event) is True
    h.handle(installation_event["data"])
    assert mock_install_slack_integration.call_args.args == (organization, user, installation_event["data"]["payload"])
