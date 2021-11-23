const int clk_1 = 15;
const int dt_1 = 4;
const int input_1 = 33;
int rot_position_1 = 0;

int rotation_1;
int clk_val_1;
int dt_val_1;
int rot_button_1;


const int clk_2 = 4;
const int dt_2 = 18;
const int input_2 = 32;
int rot_position_2 = 0;

int rotation_2;
int clk_val_2;
int dt_val_2;
int rot_button_2;


const int clk_3 = 19;
const int dt_3 = 21;
const int input_3 = 35;
int rot_position_3 = 0;

int rotation_3;
int clk_val_3;
int dt_val_3;
int rot_button_3;


const int clk_4 = 22;
const int dt_4 = 23;
const int input_4 = 34;
int rot_position_4 = 0;

int rotation_4;
int clk_val_4;
int dt_val_4;
int rot_button_4;


void setup(void){
  Serial.begin(9600); 
  Serial.println("start");
  
  pinMode(clk_1, INPUT);
  pinMode(dt_1, INPUT);
  pinMode(input_1, INPUT);

  pinMode(clk_2, INPUT);
  pinMode(dt_2, INPUT);
  pinMode(input_2, INPUT);

  pinMode(clk_3, INPUT);
  pinMode(dt_3, INPUT);
  pinMode(input_3, INPUT);

  pinMode(clk_4, INPUT);
  pinMode(dt_4, INPUT);
  pinMode(input_4, INPUT);
  
  rotation_1 = digitalRead(clk_1);
  rotation_2 = digitalRead(clk_2);
  rotation_3 = digitalRead(clk_3);
  rotation_4 = digitalRead(clk_4);
}

void loop(void) {
//  Serial.println(digitalRead(5));
  clk_val_1 = digitalRead(clk_1);
  clk_val_2 = digitalRead(clk_2);
  clk_val_3 = digitalRead(clk_3);
  clk_val_4 = digitalRead(clk_4);

  dt_val_1 = digitalRead(dt_1);
  dt_val_2 = digitalRead(dt_2);
  dt_val_3 = digitalRead(dt_3);
  dt_val_4 = digitalRead(dt_4);
  
  rot_button_1 = digitalRead(input_1);
  rot_button_2 = digitalRead(input_2);
  rot_button_3 = digitalRead(input_3);
  rot_button_4 = digitalRead(input_4);

//  Serial.println("CLK");
//  Serial.print(clk_val_1); Serial.print(" : ");
//  Serial.print(clk_val_2); Serial.print(" : ");
//  Serial.print(clk_val_3); Serial.print(" : ");
//  Serial.print(clk_val_4); Serial.println();
//
//  Serial.println("DT");
//  Serial.print(dt_val_1); Serial.print(" : ");
//  Serial.print(dt_val_2); Serial.print(" : ");
//  Serial.print(dt_val_3); Serial.print(" : ");
//  Serial.print(dt_val_4); Serial.println();

  if (clk_val_1 != rotation_1){
    if(digitalRead(dt_1)!=clk_val_1){
      rot_position_1++;}
    else{rot_position_1--;}}
  rotation_1 = clk_val_1;
  Serial.println(rot_position_1);

//  Serial.println("Rotary Button");
//  Serial.print(rot_button_1);  Serial.print(" : ");
//  Serial.print(rot_button_2);  Serial.print(" : ");
//  Serial.print(rot_button_3);  Serial.print(" : ");
//  Serial.print(rot_button_4);  Serial.println();

//  Serial.println("Rotation");
//  Serial.print(rot_position_1); Serial.print(" : ");
//  Serial.print(rot_position_2); Serial.print(" : ");
//  Serial.print(rot_position_3); Serial.print(" : ");
//  Serial.print(rot_position_4); Serial.println();

  Serial.println("-----");
}
