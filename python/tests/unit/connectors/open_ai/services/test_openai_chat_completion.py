# Copyright (c) Microsoft. All rights reserved.


import pytest
from pydantic import ValidationError

from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.open_ai.const import USER_AGENT
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import OpenAIChatCompletion


def test_open_ai_chat_completion_init() -> None:
    ai_model_id = "test_model_id"
    api_key = "test_api_key"

    # Test successful initialization
    open_ai_chat_completion = OpenAIChatCompletion(
        ai_model_id=ai_model_id,
        api_key=api_key,
    )

    assert open_ai_chat_completion.ai_model_id == ai_model_id
    assert isinstance(open_ai_chat_completion, ChatCompletionClientBase)


def test_open_ai_chat_completion_init_with_default_header() -> None:
    ai_model_id = "test_model_id"
    api_key = "test_api_key"
    default_headers = {"X-Unit-Test": "test-guid"}

    # Test successful initialization
    open_ai_chat_completion = OpenAIChatCompletion(
        ai_model_id=ai_model_id,
        api_key=api_key,
        default_headers=default_headers,
    )

    assert open_ai_chat_completion.ai_model_id == ai_model_id
    assert isinstance(open_ai_chat_completion, ChatCompletionClientBase)

    # Assert that the default header we added is present in the client's default headers
    for key, value in default_headers.items():
        assert key in open_ai_chat_completion.client.default_headers
        assert open_ai_chat_completion.client.default_headers[key] == value


def test_open_ai_chat_completion_init_with_empty_model_id() -> None:
    # ai_model_id = "test_model_id"
    api_key = "test_api_key"

    with pytest.raises(ValidationError, match="ai_model_id"):
        OpenAIChatCompletion(
            ai_model_id="",
            api_key=api_key,
        )


def test_open_ai_chat_completion_init_with_empty_api_key() -> None:
    ai_model_id = "test_model_id"
    # api_key = "test_api_key"

    with pytest.raises(ValidationError, match="api_key"):
        OpenAIChatCompletion(
            ai_model_id=ai_model_id,
            api_key="",
        )


def test_open_ai_chat_completion_serialize() -> None:
    ai_model_id = "test_model_id"
    api_key = "test_api_key"
    default_headers = {"X-Unit-Test": "test-guid"}

    settings = {
        "ai_model_id": ai_model_id,
        "api_key": api_key,
        "default_headers": default_headers,
    }

    open_ai_chat_completion = OpenAIChatCompletion.from_dict(settings)
    dumped_settings = open_ai_chat_completion.to_dict()
    assert dumped_settings["ai_model_id"] == ai_model_id
    assert dumped_settings["api_key"] == api_key
    # Assert that the default header we added is present in the dumped_settings default headers
    for key, value in default_headers.items():
        assert key in dumped_settings["default_headers"]
        assert dumped_settings["default_headers"][key] == value
    # Assert that the 'User-agent' header is not present in the dumped_settings default headers
    assert USER_AGENT not in dumped_settings["default_headers"]


def test_open_ai_chat_completion_serialize_with_org_id() -> None:
    ai_model_id = "test_model_id"
    api_key = "test_api_key"
    org_id = "test_org_id"

    settings = {
        "ai_model_id": ai_model_id,
        "api_key": api_key,
        "org_id": org_id,
    }

    open_ai_chat_completion = OpenAIChatCompletion.from_dict(settings)
    dumped_settings = open_ai_chat_completion.to_dict()
    assert dumped_settings["ai_model_id"] == ai_model_id
    assert dumped_settings["api_key"] == api_key
    assert dumped_settings["org_id"] == org_id
    # Assert that the 'User-agent' header is not present in the dumped_settings default headers
    assert USER_AGENT not in dumped_settings["default_headers"]
