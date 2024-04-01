int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;

// LED Variables
unsigned long before_time = 0;
const int LED_PIN_RED = 13;
const int LED_PIN_YELLOW = 27;
const int LED_PIN_GREEN = 12;
int LED = LOW;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  sending = false;
  writeDisplay("Sleep", 0, true);

  pinMode(LED_PIN_RED, OUTPUT);
  pinMode(LED_PIN_YELLOW, OUTPUT);
  pinMode(LED_PIN_GREEN, OUTPUT);
}

void loop() {
  String command = receiveMessage();
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  else if(command == "0"){
    before_time = millis();
    digitalWrite(LED_PIN_RED, HIGH);
  }
  else if(command == "1"){
    before_time = millis();
    digitalWrite(LED_PIN_YELLOW, HIGH);
  }
  else if(command == "2"){
    before_time = millis();
    digitalWrite(LED_PIN_GREEN, HIGH);
  }

  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);    
  }

  if(millis() - before_time >= 500){
    digitalWrite(LED_PIN_RED, LOW); //Turn off LED
    digitalWrite(LED_PIN_YELLOW, LOW); //Turn off LED
    digitalWrite(LED_PIN_GREEN, LOW); //Turn off LED
  }
}
