from src.rules_engine import RulesEngine
from src.mqtt_client import MQTTClient

if __name__ == "__main__":
  # topic ID
  topic_id = "77ec8396-e265-455a-bf4b-8a7a07eb3c84"
  
  # Initialize the rules engine
  rules_engine = RulesEngine()

  # Initialize and start the MQTT client
  mqtt_client = MQTTClient(topic_id, rules_engine)
  mqtt_client.start()