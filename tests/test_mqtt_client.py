from unittest.mock import MagicMock
from src.mqtt_client import MQTTClient

def test_mqtt_client_message_handling():
  # Test topic ID
  topic_id = "5123fd09-c862-4595-80e5-4b595fbff11c"

  # Mock RulesEngine. We only care about setting up the return value
  # since it will be used in mqtt_client.on_message method.
  mock_rules_engine = MagicMock()
  mock_rules_engine.calculate.return_value = {
    "id": "test123",
    "isEligible": True,
    "baseAmount": 60.0,
    "childrenAmount": 0.0,
    "supplementAmount": 60.0
  }

  # Initialize MQTTClient with mocked RulesEngine
  mqtt_client = MQTTClient(topic_id, mock_rules_engine)
  mqtt_client.client = MagicMock()  # Mock the internal MQTT client

  # Simulate receiving a message
  mock_msg = MagicMock()
  mock_msg.payload.decode.return_value = '{"id": "test123", "familyComposition": "single", "numberOfChildren": 0, "familyUnitInPayForDecember": true}'
  mock_msg.topic = f"BRE/calculateWinterSupplementInput/{topic_id}"

  # Call the on_message method directly
  mqtt_client.on_message(None, None, mock_msg)

  # Assert that the rules engine was called with the correct input
  mock_rules_engine.calculate.assert_called_once_with({
    "id": "test123",
    "familyComposition": "single",
    "numberOfChildren": 0,
    "familyUnitInPayForDecember": True
  })

  # Assert that the output was published to the correct output topic
  mqtt_client.client.publish.assert_called_once_with(
    f"BRE/calculateWinterSupplementOutput/{topic_id}",
    '{"id": "test123", "isEligible": true, "baseAmount": 60.0, "childrenAmount": 0.0, "supplementAmount": 60.0}'
  )
