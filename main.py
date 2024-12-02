import argparse
from src.rules_engine import RulesEngine
from src.mqtt_client import MQTTClient

def main():
  # Parse command-line arguments
  parser = argparse.ArgumentParser(description="Run the Winter Supplement Rules Engine MQTT Client.")
  parser.add_argument(
    "--topic-id",
    required=True,
    help="The unique MQTT topic ID generated by the Winter Supplement web app.",
  )
  args = parser.parse_args()
  
  # Retrieve the topic ID
  topic_id = args.topic_id
  
  # Initialize the rules engine
  rules_engine = RulesEngine()

  # Initialize and start the MQTT client
  mqtt_client = MQTTClient(topic_id, rules_engine)
  try:
    mqtt_client.start()
  except KeyboardInterrupt:
    mqtt_client.stop()


if __name__ == "__main__":
  main()