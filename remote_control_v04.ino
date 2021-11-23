#include "PubSubClient.h"
#include "WiFi.h"

const char* ssid = "CALVIN-Student";
const char* password = "CITStudentsOnly";

const char* mqtt_server = "10.252.243.158";
const char* topic = "channel";
const char* clientID = "proyek6_remote";
const char* mqtt_username = "jm03";
const char* mqtt_password = "191900103";

int to_send;
char to_send_str[5];

WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient);
const int button1 = 4;
int button1_state;

const int mode_button = 26;
int comm_mode = 0;

const int clk_1 = 15;
const int dt_1 = 2;
int rot_position_1 = 0;
int rotation_1;
int value_1;
int dt_val_1;

const int clk_2 = 5;
const int dt_2 = 18;
int rot_position_2 = 0;
int rotation_2;
int value_2;
int dt_val_2;

const int clk_3 = 19;
const int dt_3 = 21;
int rot_position_3 = 0;
int rotation_3;
int value_3;
int dt_val_3;

const int clk_4 = 22;
const int dt_4 = 23;
int rot_position_4 = 0;
int rotation_4;
int value_4;
int dt_val_4;

int ch1_control;
int ch2_control;
int ch3_control;
int ch4_control;

void connect_mqtt(){
  if(client.connect(clientID, mqtt_username, mqtt_password)){
    Serial.println("Connected to MQTT broker");
  }
  else{Serial.println("Failed to connect to MQTT Broker");}}

void setup(void){
  Serial.begin(9600); 
  Serial.println("start");
  WiFi.disconnect();
  pinMode(mode_button, INPUT);
  
  pinMode(button1, INPUT_PULLUP);
  pinMode(clk_1, INPUT);
  pinMode(dt_1, INPUT);

  pinMode(clk_2, INPUT);
  pinMode(dt_2, INPUT);

  pinMode(clk_3, INPUT);
  pinMode(dt_3, INPUT);

  pinMode(clk_4, INPUT);
  pinMode(dt_4, INPUT);

  rotation_1 = digitalRead(clk_1);
  rotation_2 = digitalRead(clk_2);
  rotation_3 = digitalRead(clk_3);
  rotation_4 = digitalRead(clk_4);
  Serial.println("Checkpoint 1");
  WiFi.begin(ssid, password);
  while(WiFi.status()!=WL_CONNECTED){
    delay(500);
    Serial.println("...");
    }
  connect_mqtt();
  Serial.println("Checkpoint 2");
  Serial.println(WiFi.localIP());
}

void loop(void) {
  
  comm_mode = digitalRead(mode_button);
  
  // Serial.setTimeout(1000);
  button1_state = digitalRead(button1);
  value_1 = digitalRead(clk_1);
  value_2 = digitalRead(clk_2);
  value_3 = digitalRead(clk_3);
  value_4 = digitalRead(clk_4);

  dt_val_1 = digitalRead(dt_1);
  dt_val_2 = digitalRead(dt_2);
  dt_val_3 = digitalRead(dt_3);
  dt_val_4 = digitalRead(dt_4);

  // Serial.print(value); Serial.print(" : "); Serial.println(dt_val);
  if (value_1 != rotation_1){
    if (digitalRead(dt_1) != value_1){
      rot_position_1++;} 
    else {rot_position_1--;}}
  
  if (value_2 != rotation_2){
    if (digitalRead(dt_2) != value_2){
      rot_position_2++;} 
    else {rot_position_2--;}}
  
  if (value_3 != rotation_3){
    if (digitalRead(dt_3) != value_3){
      rot_position_3++;} 
    else {rot_position_3--;}}
      
  if (value_4 != rotation_4){
    if (digitalRead(dt_4) != value_4){
      rot_position_4++;} 
    else {rot_position_4--;}}
  
  if (comm_mode == HIGH){
    rot_position_1 = 0;
    rot_position_2 = 0;
    rot_position_3 = 0;
    rot_position_4 = 0;
    delay(1000);
    }    
  Serial.println(button1_state);
  Serial.print(rot_position_1); Serial.print(" : ");
  Serial.print(rot_position_2); Serial.print(" : ");
  Serial.print(rot_position_3); Serial.print(" : ");
  Serial.print(rot_position_4); Serial.println();

  String strdata = String((int)button1_state)
  + ":" + String((int)rot_position_1) 
  + ":" + String((int)rot_position_2) 
  + ":" + String((int)rot_position_3)
  + ":" + String((int)rot_position_4);
  

  if (client.publish(topic, strdata.c_str())){
    Serial.println("Sent");
    }
  else{
    Serial.println("failed to send");
    client.connect(clientID, mqtt_username, mqtt_password);
    client.publish(topic, strdata.c_str());
    Serial.println("CH1 Sent");
    }
  // client.disconnect();
  delay(50);
  
  rotation_1 = value_1;
  rotation_2 = value_2;
  rotation_3 = value_3;
  rotation_4 = value_4;
  
}
