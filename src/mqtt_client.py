import paho.mqtt.client as mqtt
import json
import logging

logger = logging.getLogger(__name__)

class MQTTClient:
  def __init__(self, topic_id, rules_engine):
    """
    Initializes the MQTT client.

    Args:
      topic_id (string): Topic ID to set up the input topic with.
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
    logger.info(f"Initialized MQTT client with topics: {self.input_topic}, {self.output_topic}")

  def on_message(self, client, userdata, msg):
    """
    Callback for when a message is received.

    Args:
      client: MQTT client instance (not used).
      userdata: User data (not used).
      msg: MQTT message object.
    """

    try:
      input_data = json.loads(msg.payload.decode())
      logger.info(f"Received message: {input_data}")
      
      # Process data using the rules engine
      output_data = self.rules_engine.calculate(input_data)
      logger.info(f"Processed output: {output_data}")
      
      # Publish the result to the output topic
      topic = f"{self.output_topic}"
      self.client.publish(topic, json.dumps(output_data))
      logger.info(f"Published result to topic: {topic}")
    except Exception as e:
      logger.error(f"Error processing message: {e}")

  def start(self):
    """
    Connects to the MQTT broker and starts listening.
    """

    self.client.on_message = self.on_message
    self.client.connect(self.broker, self.port)

    # Subscribe to input topic
    self.client.subscribe(f"{self.input_topic}")
    logger.info(f"Subscribed to topic: {self.input_topic}")

    self.client.loop_forever()
  
  def stop(self):
    """
    Stops the MQTT client gracefully.
    """

    logger.info("Stopping MQTT client...")
    self.client.loop_stop()  # Stops the loop
    self.client.disconnect()  # Disconnects from the broker
    logger.info("MQTT client stopped.")
