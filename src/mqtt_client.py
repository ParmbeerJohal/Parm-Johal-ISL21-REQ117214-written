import paho.mqtt.client as mqtt

class MQTTClient:
  def __init__(self, topic_id, rules_engine):
    """
    Initializes the MQTT client.

    Args:
      rules_engine (RulesEngine): Instance of the RulesEngine class.
    """
    
    self.topic_id = topic_id
    if not self.topic_id:
      raise ValueError("MQTT_TOPIC_ID not provided")
    
    self.rules_engine = rules_engine
    self.broker = "test.mosquitto.org"
    self.port = 1883
    self.input_topic = f"BRE/calculateWinterSupplementInput/{self.topic_id}"
    self.output_topic = f"BRE/calculateWinterSupplementOutput/{self.topic_id}"

    self.client = mqtt.Client()