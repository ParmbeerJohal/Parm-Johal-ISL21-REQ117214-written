import paho.mqtt.client as mqtt
import json

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

  def on_message(self, client, userdata, msg):
      """
      Callback for when a message is received.

      Args:
        client: MQTT client instance.
        userdata: User data.
        msg: MQTT message object.
      """
      try:
        input_data = json.loads(msg.payload.decode())
        print(f"Received message: {input_data}")
        
        # Process data using the rules engine
        output_data = self.rules_engine.calculate(input_data)
        print(f"Processed output: {output_data}")
        
        # Publish the result to the output topic
        topic = f"{self.output_topic}"
        self.client.publish(topic, json.dumps(output_data))
        print(f"Published result to topic: {topic}")
      except Exception as e:
        print(f"Error processing message: {e}")

  def start(self):
    """
    Connects to the MQTT broker and starts listening.
    """
    self.client.on_message = self.on_message
    self.client.connect(self.broker, self.port)

    # Subscribe to input topic
    self.client.subscribe(f"{self.input_topic}")
    print(f"Subscribed to topic: {self.input_topic}")

    self.client.loop_forever()
