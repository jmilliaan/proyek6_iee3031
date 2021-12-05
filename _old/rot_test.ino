int sig_a = 5;
int sig_b = 18;

int ch_a;
int ch_b;

void setup() {
  Serial.begin(9600);
  pinMode(sig_a, INPUT);
  pinMode(sig_b, INPUT);
}

void loop() {
  ch_a = digitalRead(sig_a);
  ch_b = digitalRead(sig_b);
  Serial.print(ch_a); Serial.print(" : "); Serial.println(ch_b);
  delay(100);
}
